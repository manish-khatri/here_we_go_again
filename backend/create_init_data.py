from flask import Flask
try:
    from models import db
    from models import User, Role, UserRoles, Subject, Chapter, Quiz, Question
except ImportError:
    from backend.models import db
    from backend.models import User, Role, UserRoles, Subject, Chapter, Quiz, Question
from werkzeug.security import generate_password_hash
from datetime import date, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/database.sqlite3'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'super-secret-salt'
app.config['SECURITY_JOIN_USER_ROLES'] = True
app.config['SECURITY_PASSWORD_SINGLE_HASH'] = False
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
db.init_app(app)

with app.app_context():
    db.create_all()

    # Create roles
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(id=1, name='admin')
        db.session.add(admin_role)

    user_role = Role.query.filter_by(name='customer').first()
    if not user_role:
        user_role = Role(id=2, name='customer')
        db.session.add(user_role)

    db.session.commit()

    # Create users
    admin_user = User.query.filter_by(user_mail='admin@quiz.com').first()
    if not admin_user:
        admin_user = User(
            user_id='A0', 
            user_mail='admin@quiz.com', 
            user_name='admin', 
            user_pass=generate_password_hash('admin'), 
            fs_uniquifier='admin-unique'
        )
        db.session.add(admin_user)

    user0 = User.query.filter_by(user_mail='user0@quiz.com').first()
    if not user0:
        user0 = User(
            user_id='C0', 
            user_mail='user0@quiz.com', 
            user_name='user', 
            user_pass=generate_password_hash('user'), 
            fs_uniquifier='user0-unique'
        )
        db.session.add(user0)

    db.session.commit()

    # Assign roles
    if admin_role not in admin_user.roles:
        admin_user.roles.append(admin_role)
    if user_role not in user0.roles:
        user0.roles.append(user_role)

    db.session.commit()

    # Create sample subjects
    physics = Subject.query.filter_by(sub_id='PHY001').first()
    if not physics:
        physics = Subject(sub_id='PHY001', sub_name='Physics', sub_desc='Study of matter and energy')
        db.session.add(physics)

    app_dev = Subject.query.filter_by(sub_id='APP001').first()
    if not app_dev:
        app_dev = Subject(sub_id='APP001', sub_name='App Dev-I', sub_desc='Application Development Fundamentals')
        db.session.add(app_dev)

    db.session.commit()

    # Create sample chapters
    force_chapter = Chapter.query.filter_by(chp_id='FORCE001').first()
    if not force_chapter:
        force_chapter = Chapter(chp_id='FORCE001', chp_name='Force', chp_desc='Study of forces and motion', sub_id='PHY001')
        db.session.add(force_chapter)

    emf_chapter = Chapter.query.filter_by(chp_id='EMF001').first()
    if not emf_chapter:
        emf_chapter = Chapter(chp_id='EMF001', chp_name='EMF', chp_desc='Electromagnetic forces', sub_id='PHY001')
        db.session.add(emf_chapter)

    html_chapter = Chapter.query.filter_by(chp_id='HTML001').first()
    if not html_chapter:
        html_chapter = Chapter(chp_id='HTML001', chp_name='HTML', chp_desc='HyperText Markup Language', sub_id='APP001')
        db.session.add(html_chapter)

    css_chapter = Chapter.query.filter_by(chp_id='CSS001').first()
    if not css_chapter:
        css_chapter = Chapter(chp_id='CSS001', chp_name='CSS', chp_desc='Cascading Style Sheets', sub_id='APP001')
        db.session.add(css_chapter)

    db.session.commit()

    # Create sample quizzes
    css_quiz = Quiz.query.filter_by(q_id='CSS_QUIZ_001').first()
    if not css_quiz:
        css_quiz = Quiz(
            q_id='CSS_QUIZ_001',
            q_name='CSS Basics Quiz',
            chp_id='CSS001',
            sub_id='APP001',
            date_of_quiz=date(2024, 1, 15),
            time_dur=time(0, 10, 0),
            remarks='Basic CSS concepts quiz'
        )
        db.session.add(css_quiz)

    html_quiz = Quiz.query.filter_by(q_id='HTML_QUIZ_001').first()
    if not html_quiz:
        html_quiz = Quiz(
            q_id='HTML_QUIZ_001',
            q_name='HTML Fundamentals Quiz',
            chp_id='HTML001',
            sub_id='APP001',
            date_of_quiz=date(2024, 1, 20),
            time_dur=time(0, 15, 0),
            remarks='HTML basics and structure quiz'
        )
        db.session.add(html_quiz)

    force_quiz = Quiz.query.filter_by(q_id='FORCE_QUIZ_001').first()
    if not force_quiz:
        force_quiz = Quiz(
            q_id='FORCE_QUIZ_001',
            q_name='Force and Motion Quiz',
            chp_id='FORCE001',
            sub_id='PHY001',
            date_of_quiz=date(2024, 1, 25),
            time_dur=time(0, 20, 0),
            remarks='Physics force concepts quiz'
        )
        db.session.add(force_quiz)

    db.session.commit()

    # Create sample questions for CSS quiz
    css_questions = [
        {
            'ques_id': 'CSS_Q001',
            'statement': 'What is the purpose of CSS classes?',
            'options': ['To create animations', 'To style HTML elements', 'To handle user interactions', 'To store data'],
            'answer': '2'
        },
        {
            'ques_id': 'CSS_Q002',
            'statement': 'How do you apply internal CSS styles?',
            'options': ['Using <style> tag', 'Using <link> tag', 'Using <script> tag', 'Using <meta> tag'],
            'answer': '1'
        },
        {
            'ques_id': 'CSS_Q003',
            'statement': 'What does CSS stand for?',
            'options': ['Computer Style Sheets', 'Cascading Style Sheets', 'Creative Style Sheets', 'Colorful Style Sheets'],
            'answer': '2'
        }
    ]

    for q_data in css_questions:
        question = Question.query.filter_by(ques_id=q_data['ques_id']).first()
        if not question:
            question = Question(
                ques_id=q_data['ques_id'],
                sub_id='APP001',
                chp_id='CSS001',
                q_id='CSS_QUIZ_001',
                statement=q_data['statement'],
                options=q_data['options'],
                answer=q_data['answer']
            )
            db.session.add(question)

    # Create sample questions for HTML quiz
    html_questions = [
        {
            'ques_id': 'HTML_Q001',
            'statement': 'What does the <b> element do?',
            'options': ['Creates a line break', 'Makes text bold', 'Creates a paragraph', 'Adds a link'],
            'answer': '2'
        },
        {
            'ques_id': 'HTML_Q002',
            'statement': 'How many heading levels are available in HTML?',
            'options': ['4', '5', '6', '7'],
            'answer': '3'
        },
        {
            'ques_id': 'HTML_Q003',
            'statement': 'What is the purpose of the <form> element?',
            'options': ['To create tables', 'To collect user input', 'To display images', 'To play videos'],
            'answer': '2'
        }
    ]

    for q_data in html_questions:
        question = Question.query.filter_by(ques_id=q_data['ques_id']).first()
        if not question:
            question = Question(
                ques_id=q_data['ques_id'],
                sub_id='APP001',
                chp_id='HTML001',
                q_id='HTML_QUIZ_001',
                statement=q_data['statement'],
                options=q_data['options'],
                answer=q_data['answer']
            )
            db.session.add(question)

    # Create sample questions for Force quiz
    force_questions = [
        {
            'ques_id': 'FORCE_Q001',
            'statement': 'What is Newton\'s First Law also known as?',
            'options': ['Law of Action-Reaction', 'Law of Inertia', 'Law of Acceleration', 'Law of Gravity'],
            'answer': '2'
        },
        {
            'ques_id': 'FORCE_Q002',
            'statement': 'What is the SI unit of force?',
            'options': ['Joule', 'Watt', 'Newton', 'Pascal'],
            'answer': '3'
        },
        {
            'ques_id': 'FORCE_Q003',
            'statement': 'What happens to an object when balanced forces act on it?',
            'options': ['It accelerates', 'It remains at rest or constant velocity', 'It changes direction', 'It loses energy'],
            'answer': '2'
        }
    ]

    for q_data in force_questions:
        question = Question.query.filter_by(ques_id=q_data['ques_id']).first()
        if not question:
            question = Question(
                ques_id=q_data['ques_id'],
                sub_id='PHY001',
                chp_id='FORCE001',
                q_id='FORCE_QUIZ_001',
                statement=q_data['statement'],
                options=q_data['options'],
                answer=q_data['answer']
            )
            db.session.add(question)

    db.session.commit()

if __name__ == "__main__":
    print("Database initialized and admin/user seeded with sample data.")
