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
    user = User(
        user_id=data['user_mail'],
        user_mail=data['user_mail'],
        user_name=data['user_name'],
        user_pass=generate_password_hash(data['user_pass']),
        qualification=data['qualification'],
        dob=data['dob'],
        fs_uniquifier=data['user_mail']+'-unique',
        active=True
    )
    db.session.add(user)
    db.session.commit()
    # Assign 'customer' role
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
def get_subjects():
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
    quiz = Quiz(
        q_id=data['q_id'],
        q_name=data['q_name'],
        chp_id=chp_id,
        sub_id=data['sub_id'],
        date_of_quiz=data['date_of_quiz'],
        time_dur=data['time_dur'],
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
    quiz.q_name = data.get('q_name', quiz.q_name)
    quiz.date_of_quiz = data.get('date_of_quiz', quiz.date_of_quiz)
    quiz.time_dur = data.get('time_dur', quiz.time_dur)
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
        {'ques_id': q.ques_id, 'sub_id': q.sub_id, 'chp_id': q.chp_id, 'q_id': q.q_id, 'statement': q.statement, 'options': q.options, 'answer': q.answer}
        for q in questions
    ]), 200

@app.post('/api/quizzes/<q_id>/questions')
@roles_required('admin')
def create_question(q_id):
    data = request.get_json()
    required = ['ques_id', 'sub_id', 'chp_id', 'statement', 'options', 'answer']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    if Question.query.filter_by(ques_id=data['ques_id']).first():
        return jsonify({'error': 'Question already exists'}), 400
    question = Question(
        ques_id=data['ques_id'],
        sub_id=data['sub_id'],
        chp_id=data['chp_id'],
        q_id=q_id,
        statement=data['statement'],
        options=data['options'],
        answer=data['answer']
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
    question.statement = data.get('statement', question.statement)
    question.options = data.get('options', question.options)
    question.answer = data.get('answer', question.answer)
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
def admin_dashboard():
    user_count = User.query.count()
    quiz_count = Quiz.query.count()
    attempt_count = Score.query.count()
    avg_score = db.session.query(db.func.avg(Score.total_score)).scalar() or 0
    return jsonify({
        'total_users': user_count,
        'total_quizzes': quiz_count,
        'total_attempts': attempt_count,
        'average_score': avg_score
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

# ----------- CSV EXPORT ENDPOINTS -----------
@app.post('/api/export/user-scores')
@auth_required()
def trigger_user_csv_export():
    task = export_user_scores_csv.delay(current_user.user_id)
    return jsonify({'task_id': task.id, 'message': 'CSV export started'}), 202

@app.post('/api/export/all-scores')
@roles_required('admin')
def trigger_admin_csv_export():
    task = export_all_scores_csv.delay()
    return jsonify({'task_id': task.id, 'message': 'CSV export started'}), 202

@app.get('/api/export/status/<task_id>')
def check_export_status(task_id):
    from backend.celery_app import celery
    task = celery.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        filename = task.result
        return jsonify({'state': task.state, 'filename': filename, 'download_url': f'/api/export/download/{filename}'}), 200
    return jsonify({'state': task.state}), 200

@app.get('/api/export/download/<filename>')
def download_export(filename):
    # Security: only allow files from EXPORT_DIR
    if not os.path.exists(os.path.join(EXPORT_DIR, filename)):
        return jsonify({'error': 'File not found'}), 404
    return send_from_directory(EXPORT_DIR, filename, as_attachment=True)