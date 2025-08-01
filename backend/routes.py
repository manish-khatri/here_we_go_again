from flask import current_app as app
from flask_security import auth_required
from flask import request, jsonify, session
from flask_security import current_user, login_user, logout_user
from backend.models import db, User, Role
from werkzeug.security import check_password_hash, generate_password_hash
from flask_security import SQLAlchemySessionUserDatastore
from flask_security import roles_required
from backend.models import Subject, Chapter
from backend.models import Quiz, Question
from flask_security import current_user
from backend.models import Score
from datetime import datetime
from backend.tasks import export_user_scores_csv, export_all_scores_csv
from flask import send_from_directory
import os
from backend.cache import cache, invalidate_cache, set_cache, get_cache

EXPORT_DIR = os.path.join(os.path.dirname(__file__), 'exports')

@app.get('/')
def home():
    return 'HII'

@app.get('/protected')
@auth_required()
def protected():
    return '<h1> only accessible when authenticated </h1>'

# User registration endpoint
@app.post('/api/register')
def register():
    data = request.get_json()
    required_fields = ['user_mail', 'user_name', 'user_pass', 'qualification', 'dob']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    if User.query.filter_by(user_mail=data['user_mail']).first():
        return jsonify({'error': 'User already exists'}), 400
    
    # Check if trying to register as admin
    requested_role = data.get('role', 'customer')  # Default to customer if no role specified
    if requested_role == 'admin':
        # Check if admin already exists
        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role:
            existing_admin = User.query.join(User.roles).filter(Role.name == 'admin').first()
            if existing_admin:
                return jsonify({'error': 'Admin account already exists. Only one admin is allowed.'}), 400
    
    # Convert date string to date object
    try:
        dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    user = User(
        user_id=data['user_mail'],
        user_mail=data['user_mail'],
        user_name=data['user_name'],
        user_pass=generate_password_hash(data['user_pass']),
        qualification=data['qualification'],
        dob=dob,
        fs_uniquifier=data['user_mail']+'-unique',
        active=True
    )
    db.session.add(user)
    db.session.commit()
    
    # Assign appropriate role
    if requested_role == 'admin':
        user_role = Role.query.filter_by(name='admin').first()
    else:
        user_role = Role.query.filter_by(name='customer').first()
    
    if user_role:
        user.roles.append(user_role)
        db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# User login endpoint
@app.post('/api/login')
def login():
    data = request.get_json()
    user = User.query.filter_by(user_mail=data.get('user_mail')).first()
    if user and check_password_hash(user.user_pass, data.get('user_pass')):
        login_user(user)
        return jsonify({'message': 'Login successful', 'role': [role.name for role in user.roles]}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# Admin login endpoint (no registration)
@app.post('/api/admin/login')
def admin_login():
    data = request.get_json()
    user = User.query.filter_by(user_mail=data.get('user_mail')).first()
    if user and check_password_hash(user.user_pass, data.get('user_pass')):
        # Check if user has admin role
        if any(role.name == 'admin' for role in user.roles):
            login_user(user)
            return jsonify({'message': 'Admin login successful'}), 200
        else:
            return jsonify({'error': 'Not an admin user'}), 403
    return jsonify({'error': 'Invalid credentials'}), 401

# Logout endpoint
@app.post('/api/logout')
@auth_required()
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# ----------- SUBJECTS CRUD -----------
@app.get('/api/subjects')
@cache(timeout=600, key_prefix="subjects")  # Cache for 10 minutes
def get_subjects():
    # Try cache first
    cached_result = get_cache("subjects_data")
    if cached_result:
        return jsonify(cached_result), 200
    
    subjects = Subject.query.all()
    result = []
    for s in subjects:
        chapters = Chapter.query.filter_by(sub_id=s.sub_id).all()
        chapters_data = []
        for c in chapters:
            # Count questions for this chapter
            question_count = Question.query.filter_by(chp_id=c.chp_id).count()
            chapters_data.append({
                'chp_id': c.chp_id,
                'chp_name': c.chp_name,
                'chp_desc': c.chp_desc,
                'questionCount': question_count
            })
        
        result.append({
            'sub_id': s.sub_id,
            'sub_name': s.sub_name,
            'sub_desc': s.sub_desc,
            'chapters': chapters_data
        })
    
    # Cache the result
    set_cache("subjects_data", result, 600)
    return jsonify(result), 200

@app.post('/api/subjects')
@roles_required('admin')
def create_subject():
    data = request.get_json()
    if not data.get('sub_id') or not data.get('sub_name'):
        return jsonify({'error': 'sub_id and sub_name required'}), 400
    if Subject.query.filter_by(sub_id=data['sub_id']).first():
        return jsonify({'error': 'Subject already exists'}), 400
    subject = Subject(sub_id=data['sub_id'], sub_name=data['sub_name'], sub_desc=data.get('sub_desc'))
    db.session.add(subject)
    db.session.commit()
    
    # Invalidate cache
    invalidate_cache("subjects*")
    
    return jsonify({'message': 'Subject created'}), 201

@app.put('/api/subjects/<sub_id>')
@roles_required('admin')
def update_subject(sub_id):
    subject = Subject.query.filter_by(sub_id=sub_id).first()
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404
    data = request.get_json()
    subject.sub_name = data.get('sub_name', subject.sub_name)
    subject.sub_desc = data.get('sub_desc', subject.sub_desc)
    db.session.commit()
    return jsonify({'message': 'Subject updated'}), 200

@app.delete('/api/subjects/<sub_id>')
@roles_required('admin')
def delete_subject(sub_id):
    subject = Subject.query.filter_by(sub_id=sub_id).first()
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404
    db.session.delete(subject)
    db.session.commit()
    return jsonify({'message': 'Subject deleted'}), 200

# ----------- CHAPTERS CRUD -----------
@app.get('/api/subjects/<sub_id>/chapters')
def get_chapters(sub_id):
    chapters = Chapter.query.filter_by(sub_id=sub_id).all()
    return jsonify([
        {'chp_id': c.chp_id, 'chp_name': c.chp_name, 'chp_desc': c.chp_desc, 'sub_id': c.sub_id}
        for c in chapters
    ]), 200

@app.post('/api/subjects/<sub_id>/chapters')
@roles_required('admin')
def create_chapter(sub_id):
    data = request.get_json()
    if not data.get('chp_id') or not data.get('chp_name'):
        return jsonify({'error': 'chp_id and chp_name required'}), 400
    if Chapter.query.filter_by(chp_id=data['chp_id']).first():
        return jsonify({'error': 'Chapter already exists'}), 400
    chapter = Chapter(chp_id=data['chp_id'], chp_name=data['chp_name'], chp_desc=data.get('chp_desc'), sub_id=sub_id)
    db.session.add(chapter)
    db.session.commit()
    return jsonify({'message': 'Chapter created'}), 201

@app.put('/api/chapters/<chp_id>')
@roles_required('admin')
def update_chapter(chp_id):
    chapter = Chapter.query.filter_by(chp_id=chp_id).first()
    if not chapter:
        return jsonify({'error': 'Chapter not found'}), 404
    data = request.get_json()
    chapter.chp_name = data.get('chp_name', chapter.chp_name)
    chapter.chp_desc = data.get('chp_desc', chapter.chp_desc)
    db.session.commit()
    return jsonify({'message': 'Chapter updated'}), 200

@app.delete('/api/chapters/<chp_id>')
@roles_required('admin')
def delete_chapter(chp_id):
    chapter = Chapter.query.filter_by(chp_id=chp_id).first()
    if not chapter:
        return jsonify({'error': 'Chapter not found'}), 404
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({'message': 'Chapter deleted'}), 200

# ----------- QUIZZES CRUD -----------
@app.get('/api/quizzes')
def get_all_quizzes():
    """Public endpoint for users to view all available quizzes"""
    quizzes = Quiz.query.all()
    quiz_list = []
    
    for quiz in quizzes:
        # Get question count for this quiz
        question_count = Question.query.filter_by(q_id=quiz.q_id).count()
        
        # Get subject and chapter names
        chapter = Chapter.query.filter_by(chp_id=quiz.chp_id).first()
        subject = Subject.query.filter_by(sub_id=quiz.sub_id).first()
        
        quiz_data = {
            'q_id': quiz.q_id,
            'q_name': quiz.q_name,
            'chp_id': quiz.chp_id,
            'sub_id': quiz.sub_id,
            'date_of_quiz': str(quiz.date_of_quiz),
            'time_dur': str(quiz.time_dur),
            'remarks': quiz.remarks,
            'questionCount': question_count,
            'subject': subject.sub_name if subject else 'Unknown',
            'chapter': chapter.chp_name if chapter else 'Unknown'
        }
        quiz_list.append(quiz_data)
    
    return jsonify(quiz_list), 200

@app.get('/api/chapters/<chp_id>/quizzes')
def get_quizzes(chp_id):
    quizzes = Quiz.query.filter_by(chp_id=chp_id).all()
    return jsonify([
        {'q_id': q.q_id, 'q_name': q.q_name, 'chp_id': q.chp_id, 'sub_id': q.sub_id, 'date_of_quiz': str(q.date_of_quiz), 'time_dur': str(q.time_dur), 'remarks': q.remarks}
        for q in quizzes
    ]), 200

@app.post('/api/chapters/<chp_id>/quizzes')
@roles_required('admin')
def create_quiz(chp_id):
    data = request.get_json()
    required = ['q_id', 'q_name', 'sub_id', 'date_of_quiz', 'time_dur']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    if Quiz.query.filter_by(q_id=data['q_id']).first():
        return jsonify({'error': 'Quiz already exists'}), 400
    
    # Convert date string to date object
    from datetime import datetime, time
    try:
        if isinstance(data['date_of_quiz'], str):
            quiz_date = datetime.strptime(data['date_of_quiz'], '%Y-%m-%d').date()
        else:
            quiz_date = data['date_of_quiz']
        
        # Convert duration (minutes) to time object  
        duration_minutes = int(data['time_dur'])
        hours = duration_minutes // 60
        minutes = duration_minutes % 60
        quiz_duration = time(hour=hours, minute=minutes)
        
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid date or duration format: {str(e)}'}), 400
    
    quiz = Quiz(
        q_id=data['q_id'],
        q_name=data['q_name'],
        chp_id=chp_id,
        sub_id=data['sub_id'],
        date_of_quiz=quiz_date,
        time_dur=quiz_duration,
        remarks=data.get('remarks')
    )
    db.session.add(quiz)
    db.session.commit()
    return jsonify({'message': 'Quiz created'}), 201

@app.post('/api/quizzes')
@roles_required('admin')
def create_quiz_direct():
    data = request.get_json()
    required = ['q_id', 'q_name', 'chp_id', 'date_of_quiz', 'time_dur']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    if Quiz.query.filter_by(q_id=data['q_id']).first():
        return jsonify({'error': 'Quiz already exists'}), 400
    
    # Get the sub_id from the chapter
    chapter = Chapter.query.filter_by(chp_id=data['chp_id']).first()
    if not chapter:
        return jsonify({'error': 'Chapter not found'}), 404
    
    # Convert date string to date object
    from datetime import datetime, time
    try:
        if isinstance(data['date_of_quiz'], str):
            quiz_date = datetime.strptime(data['date_of_quiz'], '%Y-%m-%d').date()
        else:
            quiz_date = data['date_of_quiz']
        
        # Convert duration (minutes) to time object  
        duration_minutes = int(data['time_dur'])
        hours = duration_minutes // 60
        minutes = duration_minutes % 60
        quiz_duration = time(hour=hours, minute=minutes)
        
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid date or duration format: {str(e)}'}), 400
    
    quiz = Quiz(
        q_id=data['q_id'],
        q_name=data['q_name'],
        chp_id=data['chp_id'],
        sub_id=chapter.sub_id,
        date_of_quiz=quiz_date,
        time_dur=quiz_duration,
        remarks=data.get('remarks')
    )
    db.session.add(quiz)
    db.session.commit()
    return jsonify({'message': 'Quiz created'}), 201

@app.put('/api/quizzes/<q_id>')
@roles_required('admin')
def update_quiz(q_id):
    quiz = Quiz.query.filter_by(q_id=q_id).first()
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    data = request.get_json()
    
    # Convert date and time if provided
    from datetime import datetime, time
    try:
        if 'date_of_quiz' in data and data['date_of_quiz']:
            if isinstance(data['date_of_quiz'], str):
                quiz.date_of_quiz = datetime.strptime(data['date_of_quiz'], '%Y-%m-%d').date()
            else:
                quiz.date_of_quiz = data['date_of_quiz']
        
        if 'time_dur' in data and data['time_dur']:
            duration_minutes = int(data['time_dur'])
            hours = duration_minutes // 60
            minutes = duration_minutes % 60
            quiz.time_dur = time(hour=hours, minute=minutes)
            
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid date or duration format: {str(e)}'}), 400
    
    quiz.q_name = data.get('q_name', quiz.q_name)
    quiz.remarks = data.get('remarks', quiz.remarks)
    db.session.commit()
    return jsonify({'message': 'Quiz updated'}), 200

@app.delete('/api/quizzes/<q_id>')
@roles_required('admin')
def delete_quiz(q_id):
    quiz = Quiz.query.filter_by(q_id=q_id).first()
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({'message': 'Quiz deleted'}), 200

# ----------- QUESTIONS CRUD -----------
@app.get('/api/quizzes/<q_id>/questions')
def get_questions(q_id):
    questions = Question.query.filter_by(q_id=q_id).all()
    return jsonify([
        {
            'qsn_id': q.ques_id,  # Map ques_id to qsn_id for frontend
            'ques_id': q.ques_id,  # Keep both for compatibility
            'sub_id': q.sub_id, 
            'chp_id': q.chp_id, 
            'q_id': q.q_id, 
            'qsn_desc': q.statement,  # Map statement to qsn_desc
            'statement': q.statement,  # Keep both for compatibility
            'question_text': q.statement,  # Alternative field name
            'options': q.options, 
            'answer': q.answer,
            'correct_option': q.answer,  # Map answer to correct_option
            # Break down options for editing compatibility
            'option_1': q.options[0] if len(q.options) > 0 else '',
            'option_2': q.options[1] if len(q.options) > 1 else '',
            'option_3': q.options[2] if len(q.options) > 2 else '',
            'option_4': q.options[3] if len(q.options) > 3 else ''
        }
        for q in questions
    ]), 200

@app.post('/api/quizzes/<q_id>/questions')
@roles_required('admin')
def create_question(q_id):
    data = request.get_json()
    
    # Check required fields from frontend
    required = ['qsn_id', 'qsn_desc', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_option']
    if not all(field in data for field in required):
        missing_fields = [field for field in required if field not in data]
        return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400
    
    # Check if question already exists
    if Question.query.filter_by(ques_id=data['qsn_id']).first():
        return jsonify({'error': 'Question already exists'}), 400
    
    # Get quiz to obtain sub_id and chp_id
    quiz = Quiz.query.filter_by(q_id=q_id).first()
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # Convert individual options to JSON array
    options = [
        data['option_1'],
        data['option_2'], 
        data['option_3'],
        data['option_4']
    ]
    
    question = Question(
        ques_id=data['qsn_id'],
        sub_id=quiz.sub_id,
        chp_id=quiz.chp_id,
        q_id=q_id,
        statement=data['qsn_desc'],
        options=options,
        answer=str(data['correct_option'])
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({'message': 'Question created'}), 201

@app.put('/api/questions/<ques_id>')
@roles_required('admin')
def update_question(ques_id):
    question = Question.query.filter_by(ques_id=ques_id).first()
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    data = request.get_json()
    
    # Update statement if provided
    if 'qsn_desc' in data:
        question.statement = data['qsn_desc']
    
    # Update options if provided
    if all(field in data for field in ['option_1', 'option_2', 'option_3', 'option_4']):
        options = [
            data['option_1'],
            data['option_2'], 
            data['option_3'],
            data['option_4']
        ]
        question.options = options
    
    # Update correct answer if provided
    if 'correct_option' in data:
        question.answer = str(data['correct_option'])
    
    db.session.commit()
    return jsonify({'message': 'Question updated'}), 200

@app.delete('/api/questions/<ques_id>')
@roles_required('admin')
def delete_question(ques_id):
    question = Question.query.filter_by(ques_id=ques_id).first()
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Question deleted'}), 200

# ----------- USER QUIZ ATTEMPT & SCORE RECORDING -----------
@app.get('/api/quizzes/<q_id>/start')
@auth_required()
def start_quiz(q_id):
    quiz = Quiz.query.filter_by(q_id=q_id).first()
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    questions = Question.query.filter_by(q_id=q_id).all()
    return jsonify({
        'q_id': quiz.q_id,
        'q_name': quiz.q_name,
        'date_of_quiz': str(quiz.date_of_quiz),
        'time_dur': str(quiz.time_dur),
        'remarks': quiz.remarks,
        'questions': [
            {
                'ques_id': q.ques_id,
                'statement': q.statement,
                'options': q.options
            } for q in questions
        ]
    }), 200

@app.post('/api/quizzes/<q_id>/submit')
@auth_required()
def submit_quiz(q_id):
    quiz = Quiz.query.filter_by(q_id=q_id).first()
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    data = request.get_json()
    answers = data.get('answers')  # {ques_id: selected_option}
    if not answers:
        return jsonify({'error': 'No answers submitted'}), 400
    questions = Question.query.filter_by(q_id=q_id).all()
    total_questions = len(questions)
    correct = 0
    for q in questions:
        if str(q.ques_id) in answers and answers[str(q.ques_id)] == q.answer:
            correct += 1
    score_value = correct / total_questions * 100 if total_questions > 0 else 0
    # Record score
    score = Score(
        score_id=f"{current_user.user_id}_{q_id}_{datetime.utcnow().isoformat()}",
        q_id=q_id,
        user_id=current_user.user_id,
        time_stamp=datetime.utcnow(),
        total_score=score_value
    )
    db.session.add(score)
    db.session.commit()
    return jsonify({'message': 'Quiz submitted', 'score': score_value, 'correct': correct, 'total': total_questions}), 200

# ----------- USER SCORES -----------
@app.get('/api/scores')
@auth_required()
def get_user_scores():
    scores = Score.query.filter_by(user_id=current_user.user_id).all()
    return jsonify([
        {'score_id': s.score_id, 'q_id': s.q_id, 'time_stamp': str(s.time_stamp), 'total_score': s.total_score}
        for s in scores
    ]), 200

@app.get('/api/scores/<q_id>')
@auth_required()
def get_user_score_for_quiz(q_id):
    score = Score.query.filter_by(user_id=current_user.user_id, q_id=q_id).order_by(Score.time_stamp.desc()).first()
    if not score:
        return jsonify({'error': 'No score found for this quiz'}), 404
    return jsonify({'score_id': score.score_id, 'q_id': score.q_id, 'time_stamp': str(score.time_stamp), 'total_score': score.total_score}), 200

# ----------- USER DASHBOARD -----------
@app.get('/api/user/dashboard')
@auth_required()
def user_dashboard():
    # Quizzes attempted
    scores = Score.query.filter_by(user_id=current_user.user_id).all()
    attempted_quiz_ids = {s.q_id for s in scores}
    # All available quizzes
    quizzes = Quiz.query.all()
    quizzes_data = [
        {'q_id': q.q_id, 'q_name': q.q_name, 'chp_id': q.chp_id, 'sub_id': q.sub_id, 'date_of_quiz': str(q.date_of_quiz)}
        for q in quizzes
    ]
    return jsonify({
        'user_id': current_user.user_id,
        'user_name': current_user.user_name,
        'attempted_quizzes': list(attempted_quiz_ids),
        'scores': [
            {'q_id': s.q_id, 'score': s.total_score, 'time_stamp': str(s.time_stamp)} for s in scores
        ],
        'all_quizzes': quizzes_data
    }), 200

# ----------- ADMIN DASHBOARD APIS -----------
@app.get('/api/admin/dashboard')
@roles_required('admin')
@cache(timeout=300, key_prefix="admin_dashboard")  # Cache for 5 minutes
def admin_dashboard():
    # Basic stats
    user_count = User.query.count()
    quiz_count = Quiz.query.count()
    attempt_count = Score.query.count()
    avg_score = db.session.query(db.func.avg(Score.total_score)).scalar() or 0
    
    # Subject-wise average scores
    subject_scores = db.session.query(
        Subject.sub_name.label('subject_name'),
        db.func.avg(Score.total_score).label('average_score')
    ).join(Quiz, Subject.sub_id == Quiz.sub_id)\
     .join(Score, Quiz.q_id == Score.q_id)\
     .group_by(Subject.sub_id, Subject.sub_name).all()
    
    # Subject-wise attempt counts
    subject_attempts = db.session.query(
        Subject.sub_name.label('subject_name'),
        db.func.count(Score.score_id).label('attempt_count')
    ).join(Quiz, Subject.sub_id == Quiz.sub_id)\
     .join(Score, Quiz.q_id == Score.q_id)\
     .group_by(Subject.sub_id, Subject.sub_name).all()
    
    # Performance over time (last 30 days)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    performance_data = db.session.query(
        db.func.date(Score.time_stamp).label('date'),
        db.func.avg(Score.total_score).label('average_score')
    ).filter(Score.time_stamp >= thirty_days_ago)\
     .group_by(db.func.date(Score.time_stamp))\
     .order_by(db.func.date(Score.time_stamp)).all()
    
    return jsonify({
        'total_users': user_count,
        'total_quizzes': quiz_count,
        'total_attempts': attempt_count,
        'average_score': round(avg_score, 2),
        'subjectScores': [
            {'subject_name': row.subject_name, 'average_score': round(row.average_score, 2)}
            for row in subject_scores
        ],
        'subjectAttempts': [
            {'subject_name': row.subject_name, 'attempt_count': row.attempt_count}
            for row in subject_attempts
        ],
        'performanceData': [
            {'date': str(row.date), 'average_score': round(row.average_score, 2)}
            for row in performance_data
        ]
    }), 200

@app.get('/api/admin/users')
@roles_required('admin')
def admin_list_users():
    q = request.args.get('q')
    query = User.query
    if q:
        query = query.filter(User.user_name.ilike(f'%{q}%') | User.user_mail.ilike(f'%{q}%'))
    users = query.all()
    return jsonify([
        {'user_id': u.user_id, 'user_mail': u.user_mail, 'user_name': u.user_name, 'qualification': u.qualification, 'dob': str(u.dob)}
        for u in users
    ]), 200

@app.get('/api/admin/quizzes')
@roles_required('admin')
def admin_list_quizzes():
    q = request.args.get('q')
    query = Quiz.query
    if q:
        query = query.filter(Quiz.q_name.ilike(f'%{q}%'))
    quizzes = query.all()
    return jsonify([
        {'q_id': quiz.q_id, 'q_name': quiz.q_name, 'chp_id': quiz.chp_id, 'sub_id': quiz.sub_id, 'date_of_quiz': str(quiz.date_of_quiz)}
        for quiz in quizzes
    ]), 200

@app.get('/api/admin/scores')
@roles_required('admin')
def admin_list_scores():
    user_id = request.args.get('user_id')
    q_id = request.args.get('q_id')
    query = Score.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if q_id:
        query = query.filter_by(q_id=q_id)
    scores = query.all()
    return jsonify([
        {'score_id': s.score_id, 'user_id': s.user_id, 'q_id': s.q_id, 'time_stamp': str(s.time_stamp), 'total_score': s.total_score}
        for s in scores
    ]), 200

@app.get('/api/admin/subjects')
@roles_required('admin')
def admin_list_subjects():
    subjects = Subject.query.all()
    return jsonify([
        {'sub_id': s.sub_id, 'sub_name': s.sub_name, 'sub_desc': s.sub_desc}
        for s in subjects
    ]), 200

@app.get('/api/admin/chapters')
@roles_required('admin')
def admin_list_chapters():
    chapters = Chapter.query.all()
    return jsonify([
        {'chp_id': c.chp_id, 'chp_name': c.chp_name, 'chp_desc': c.chp_desc, 'sub_id': c.sub_id}
        for c in chapters
    ]), 200

# ----------- CSV EXPORT ENDPOINTS -----------
@app.post('/api/export/user-scores')
@auth_required()
def trigger_user_csv_export():
    task = export_user_scores_csv.delay(current_user.user_id)
    return jsonify({
        'task_id': task.id, 
        'message': 'CSV export started. You will be notified when ready.',
        'status': 'PENDING'
    }), 202

@app.post('/api/export/all-scores')
@roles_required('admin')
def trigger_admin_csv_export():
    task = export_all_scores_csv.delay()
    return jsonify({
        'task_id': task.id, 
        'message': 'CSV export started. You will be notified when ready.',
        'status': 'PENDING'
    }), 202

@app.get('/api/export/status/<task_id>')
@auth_required()
def check_export_status(task_id):
    from backend.celery_app import celery
    task = celery.AsyncResult(task_id)
    
    response_data = {'state': task.state, 'task_id': task_id}
    
    if task.state == 'SUCCESS':
        filename = task.result
        response_data.update({
            'filename': filename,
            'download_url': f'/api/export/download/{filename}',
            'message': 'Export completed successfully! Click to download.'
        })
        return jsonify(response_data), 200
    elif task.state == 'FAILURE':
        response_data.update({
            'error': str(task.info),
            'message': 'Export failed. Please try again.'
        })
        return jsonify(response_data), 500
    else:
        response_data.update({
            'message': 'Export in progress...'
        })
        return jsonify(response_data), 200

@app.get('/api/export/download/<filename>')
@auth_required()
def download_export(filename):
    # Security: only allow files from EXPORT_DIR and validate user access
    filepath = os.path.join(EXPORT_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    # Additional security: check if user can access this file
    if not current_user.has_role('admin') and current_user.user_id not in filename:
        return jsonify({'error': 'Access denied'}), 403
        
    return send_from_directory(EXPORT_DIR, filename, as_attachment=True)

# ----------- FORM VALIDATION ENDPOINTS -----------
@app.post('/api/validate/email')
def validate_email():
    """Validate email format and uniqueness"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({'valid': False, 'error': 'Email is required'}), 400
    
    # Basic email format validation
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return jsonify({'valid': False, 'error': 'Invalid email format'}), 400
    
    # Check uniqueness
    existing_user = User.query.filter_by(user_mail=email).first()
    if existing_user:
        return jsonify({'valid': False, 'error': 'Email already registered'}), 400
    
    return jsonify({'valid': True, 'message': 'Email is valid'}), 200

@app.get('/api/check/admin-exists')
def check_admin_exists():
    """Check if an admin account already exists"""
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role:
        existing_admin = User.query.join(User.roles).filter(Role.name == 'admin').first()
        return jsonify({'exists': bool(existing_admin)}), 200
    return jsonify({'exists': False}), 200

@app.post('/api/validate/quiz-data')
@roles_required('admin')
def validate_quiz_data():
    """Validate quiz creation data"""
    data = request.get_json()
    errors = []
    
    # Required fields
    required_fields = ['q_id', 'q_name', 'chp_id', 'sub_id', 'date_of_quiz', 'time_dur']
    for field in required_fields:
        if not data.get(field):
            errors.append(f'{field} is required')
    
    # Check if quiz ID already exists
    if data.get('q_id') and Quiz.query.filter_by(q_id=data['q_id']).first():
        errors.append('Quiz ID already exists')
    
    # Validate chapter exists
    if data.get('chp_id') and not Chapter.query.filter_by(chp_id=data['chp_id']).first():
        errors.append('Chapter does not exist')
    
    if errors:
        return jsonify({'valid': False, 'errors': errors}), 400
    
    return jsonify({'valid': True, 'message': 'Quiz data is valid'}), 200


# ----------- USER SUMMARY API -----------
@app.get('/api/user/summary')
@auth_required()
def user_summary():
    user_id = current_user.user_id
    
    # Get all scores for the user
    scores = Score.query.filter_by(user_id=user_id).all()
    
    if not scores:
        return jsonify({
            'subject_wise_quizzes': [],
            'month_wise_attempts': [],
            'total_attempts': 0,
            'average_score': 0
        }), 200
    
    # Subject-wise quiz attempts
    subject_attempts = db.session.query(
        Subject.sub_name.label('subject_name'),
        db.func.count(Score.score_id).label('attempt_count')
    ).join(Quiz, Subject.sub_id == Quiz.sub_id)\
     .join(Score, Quiz.q_id == Score.q_id)\
     .filter(Score.user_id == user_id)\
     .group_by(Subject.sub_id, Subject.sub_name).all()
    
    # Month-wise quiz attempts (last 12 months)
    from datetime import datetime, timedelta
    from sqlalchemy import extract
    
    current_date = datetime.now()
    twelve_months_ago = current_date - timedelta(days=365)
    
    month_attempts = db.session.query(
        extract('month', Score.time_stamp).label('month'),
        extract('year', Score.time_stamp).label('year'),
        db.func.count(Score.score_id).label('attempt_count')
    ).filter(
        Score.user_id == user_id,
        Score.time_stamp >= twelve_months_ago
    ).group_by(
        extract('month', Score.time_stamp),
        extract('year', Score.time_stamp)
    ).all()
    
    # Calculate statistics
    total_attempts = len(scores)
    average_score = sum(score.total_score for score in scores) / total_attempts if scores else 0
    
    # Format month names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    return jsonify({
        'subject_wise_quizzes': [
            {
                'subject_name': attempt.subject_name,
                'attempt_count': attempt.attempt_count
            } for attempt in subject_attempts
        ],
        'month_wise_attempts': [
            {
                'month': attempt.month,
                'year': attempt.year,
                'month_name': month_names.get(attempt.month, f'Month {attempt.month}'),
                'attempt_count': attempt.attempt_count
            } for attempt in month_attempts
        ],
        'total_attempts': total_attempts,
        'average_score': round(average_score, 2)
    }), 200


# ----------- INDIVIDUAL QUIZ RESULT APIS -----------
@app.get('/api/scores/<quiz_id>')
@auth_required()
def get_quiz_result(quiz_id):
    """Get detailed result for a specific quiz attempt by the current user"""
    user_id = current_user.user_id
    
    # Get the quiz result for this user and quiz
    score = Score.query.filter_by(user_id=user_id, q_id=quiz_id).first()
    
    if not score:
        return jsonify({'error': 'Quiz result not found'}), 404
    
    # Get quiz details
    quiz = Quiz.query.filter_by(q_id=quiz_id).first()
    subject = None
    chapter = None
    
    if quiz:
        if quiz.sub_id:
            subject = Subject.query.filter_by(sub_id=quiz.sub_id).first()
        if quiz.chp_id:
            chapter = Chapter.query.filter_by(chp_id=quiz.chp_id).first()
    
    # Get total questions count for this quiz
    total_questions = Question.query.filter_by(q_id=quiz_id).count()
    print(f"DEBUG: Quiz ID: {quiz_id}, Total Questions: {total_questions}, Score: {score.total_score}")
    
    # Calculate correct answers based on score percentage
    if total_questions > 0 and score.total_score > 0:
        correct_answers = round((score.total_score / 100) * total_questions)
        print(f"DEBUG: Calculated correct answers: {correct_answers}")
    else:
        correct_answers = 0
    
    return jsonify({
        'q_id': score.q_id,
        'quiz_name': quiz.q_name if quiz else quiz_id,
        'total_score': score.total_score,
        'time_stamp': score.time_stamp.isoformat() if score.time_stamp else None,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'subject': subject.sub_name if subject else None,
        'chapter': chapter.chp_name if chapter else None,
        'time_taken': getattr(score, 'time_taken', None)
    }), 200


@app.get('/api/scores/<quiz_id>/details')
@auth_required()
def get_quiz_result_details(quiz_id):
    """Get detailed question-by-question breakdown for a quiz attempt"""
    user_id = current_user.user_id
    
    # Check if user has taken this quiz
    score = Score.query.filter_by(user_id=user_id, q_id=quiz_id).first()
    if not score:
        return jsonify({'error': 'Quiz result not found'}), 404
    
    # Get all questions for this quiz
    questions = Question.query.filter_by(q_id=quiz_id).all()
    
    # For now, we'll return mock detailed data since we don't store individual answers
    # In a real implementation, you'd store user answers for each question
    question_details = []
    for i, question in enumerate(questions):
        # Mock data - in reality this would come from a user_answers table
        is_correct = i < len(questions) * (score.total_score / 100)
        
        question_details.append({
            'qsn_id': question.ques_id,
            'question_text': question.statement,
            'user_answer': 'Mock Answer',  # Mock user answer - would come from user_answers table
            'correct_answer': question.answer,
            'is_correct': is_correct
        })
    
    return jsonify({
        'quiz_id': quiz_id,
        'questions': question_details
    }), 200