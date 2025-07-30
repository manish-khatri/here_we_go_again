import csv
import os
from datetime import datetime
from backend.celery_app import celery
from backend.models import db, User, Score, Quiz
from flask import current_app

EXPORT_DIR = os.path.join(os.path.dirname(__file__), 'exports')
os.makedirs(EXPORT_DIR, exist_ok=True)

@celery.task()
def export_user_scores_csv(user_id):
    scores = Score.query.filter_by(user_id=user_id).all()
    filename = f'user_{user_id}_scores_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.csv'
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Quiz ID', 'Quiz Name', 'Score', 'Timestamp'])
        for s in scores:
            quiz = Quiz.query.filter_by(q_id=s.q_id).first()
            writer.writerow([s.q_id, quiz.q_name if quiz else '', s.total_score, s.time_stamp])
    return filename

@celery.task()
def export_all_scores_csv():
    scores = Score.query.all()
    filename = f'all_scores_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.csv'
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User ID', 'Quiz ID', 'Quiz Name', 'Score', 'Timestamp'])
        for s in scores:
            quiz = Quiz.query.filter_by(q_id=s.q_id).first()
            writer.writerow([s.user_id, s.q_id, quiz.q_name if quiz else '', s.total_score, s.time_stamp])
    return filename 