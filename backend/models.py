from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash

db=SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    # user_type = db.Column(db.String, nullable=False, default="customer")
    password = db.Column(db.String, nullable=False)
    qualification = db.Column(db.String)
    dob = db.Column(db.Date)

    scores = db.relationship('Score', backref='user', cascade='all, delete-orphan')

    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    active = db.Column(db.Boolean, default = True)
    roles = db.relationship('Role', backref='bearers', secondary='user_roles')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique=True, nullable=False)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id=db.Column(db.String, db.ForeignKey('users.id'))
    role_id=db.Column(db.String, db.ForeignKey('role.id'))


class Subject(db.Model): 
    __tablename__ = 'subject'

    sub_id = db.Column(db.String, primary_key=True, nullable=False)
    sub_name = db.Column(db.String, nullable=False)
    sub_desc = db.Column(db.String)

    chapters = db.relationship('Chapter', backref='subject', cascade='all, delete-orphan')
    questions = db.relationship('Question', backref='subject', cascade='all, delete-orphan')


class Chapter(db.Model):
    __tablename__ = 'chapter'

    chp_id = db.Column(db.String, primary_key=True, nullable=False)
    chp_name = db.Column(db.String, nullable=False)
    chp_desc = db.Column(db.String)
    sub_id = db.Column(db.String, db.ForeignKey('subject.sub_id'), nullable=False)

    quizzes = db.relationship('Quiz', backref='chapter', cascade='all, delete-orphan')
    questions = db.relationship('Question', backref='chapter', cascade='all, delete-orphan')


class Quiz(db.Model):
    __tablename__ = 'quiz'

    q_id = db.Column(db.String, primary_key=True, nullable=False)
    q_name = db.Column(db.String, nullable=False)
    chp_id = db.Column(db.String, db.ForeignKey('chapter.chp_id'), nullable=False)
    sub_id = db.Column(db.String, db.ForeignKey('subject.sub_id'), nullable=False)
    date_of_quiz = db.Column(db.Date)
    time_dur = db.Column(db.Time)

    scores = db.relationship('Score', backref='quiz', cascade='all, delete-orphan')


class Question(db.Model):
    __tablename__ = 'question'

    ques_id = db.Column(db.String, primary_key=True, nullable=False)
    sub_id = db.Column(db.String, db.ForeignKey('subject.sub_id'), nullable=False)
    chp_id = db.Column(db.String, db.ForeignKey('chapter.chp_id'), nullable=False)
    q_id = db.Column(db.String, db.ForeignKey('quiz.q_id'), nullable=False)
    statement = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)
    answer = db.Column(db.String, nullable=False)


class Score(db.Model):
    __tablename__ = 'score'

    score_id = db.Column(db.String, primary_key=True, nullable=False)
    q_id = db.Column(db.String, db.ForeignKey('quiz.q_id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False) #user_id
    time_stamp = db.Column(db.DateTime)
    total_score = db.Column(db.Float)