import csv
import os
import smtplib
from datetime import datetime, timedelta, date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from backend.celery_app import celery
from backend.models import db, User, Score, Quiz, Question, Subject, Chapter
from flask import current_app
import requests
import calendar
from collections import defaultdict

EXPORT_DIR = os.path.join(os.path.dirname(__file__), 'exports')
REPORTS_DIR = os.path.join(os.path.dirname(__file__), 'reports')
os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Email configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'your-email@gmail.com',  # Configure this
    'password': 'your-app-password',  # Configure this
}

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

# SCHEDULED JOBS

@celery.task()
def send_daily_reminders():
    """Daily reminder task - Check for inactive users and new quizzes"""
    try:
        # Get all users
        users = User.query.filter(User.roles.any(name='user')).all()
        
        # Check for users who haven't attempted any quiz in last 3 days
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        
        for user in users:
            last_attempt = Score.query.filter_by(user_id=user.user_id)\
                                   .order_by(Score.time_stamp.desc()).first()
            
            should_remind = False
            if not last_attempt:
                should_remind = True  # Never attempted any quiz
            elif last_attempt.time_stamp < three_days_ago:
                should_remind = True  # No attempt in last 3 days
            
            if should_remind:
                # Check if there are new quizzes available
                available_quizzes = Quiz.query.filter(
                    Quiz.date_of_quiz >= date.today()
                ).count()
                
                if available_quizzes > 0:
                    send_reminder_notification(user, available_quizzes)
        
        return f"Daily reminders sent to inactive users"
    except Exception as e:
        current_app.logger.error(f"Daily reminder task failed: {e}")
        return f"Failed: {e}"

def send_reminder_notification(user, quiz_count):
    """Send reminder via email or webhook"""
    try:
        # Option 1: Send Email
        send_reminder_email(user, quiz_count)
        
        # Option 2: Send via Google Chat Webhook (if configured)
        # send_gchat_reminder(user, quiz_count)
        
    except Exception as e:
        current_app.logger.error(f"Failed to send reminder to {user.user_mail}: {e}")

def send_reminder_email(user, quiz_count):
    """Send reminder email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['email']
        msg['To'] = user.user_mail
        msg['Subject'] = "Quiz Master - Don't Miss Out on New Quizzes!"
        
        body = f"""
        Hi {user.user_name},
        
        We noticed you haven't taken any quizzes recently. 
        There are {quiz_count} new quizzes available for you to attempt!
        
        Visit the Quiz Master application to:
        - Explore new quizzes
        - Test your knowledge
        - Track your progress
        
        Login now: http://localhost:5173
        
        Happy Learning!
        Quiz Master Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['email'], user.user_mail, text)
        server.quit()
        
    except Exception as e:
        current_app.logger.warning(f"Email reminder failed: {e}")

def send_gchat_reminder(user, quiz_count):
    """Send reminder via Google Chat Webhook"""
    webhook_url = "YOUR_GOOGLE_CHAT_WEBHOOK_URL"  # Configure this
    
    message = {
        "text": f"🔔 Reminder for {user.user_name}:\n"
                f"You have {quiz_count} new quizzes waiting!\n"
                f"Visit Quiz Master to continue learning."
    }
    
    try:
        response = requests.post(webhook_url, json=message)
        if response.status_code != 200:
            current_app.logger.warning(f"Google Chat webhook failed: {response.status_code}")
    except Exception as e:
        current_app.logger.warning(f"Google Chat reminder failed: {e}")

@celery.task()
def generate_monthly_reports():
    """Generate and send monthly activity reports"""
    try:
        current_date = datetime.utcnow()
        last_month = current_date.replace(day=1) - timedelta(days=1)
        month_start = last_month.replace(day=1)
        month_end = current_date.replace(day=1) - timedelta(days=1)
        
        users = User.query.filter(User.roles.any(name='user')).all()
        
        for user in users:
            report_data = generate_user_monthly_report(user, month_start, month_end)
            if report_data['quiz_count'] > 0:  # Only send if user was active
                send_monthly_report_email(user, report_data, last_month)
        
        return f"Monthly reports generated for {last_month.strftime('%B %Y')}"
    except Exception as e:
        current_app.logger.error(f"Monthly report task failed: {e}")
        return f"Failed: {e}"

def generate_user_monthly_report(user, month_start, month_end):
    """Generate monthly report data for a user"""
    # Get user's scores for the month
    monthly_scores = Score.query.filter(
        Score.user_id == user.user_id,
        Score.time_stamp >= month_start,
        Score.time_stamp <= month_end
    ).all()
    
    if not monthly_scores:
        return {'quiz_count': 0}
    
    # Calculate statistics
    quiz_count = len(monthly_scores)
    total_score = sum(score.total_score for score in monthly_scores)
    average_score = total_score / quiz_count if quiz_count > 0 else 0
    
    # Get best and worst scores
    best_score = max(score.total_score for score in monthly_scores)
    worst_score = min(score.total_score for score in monthly_scores)
    
    # Subject-wise performance
    subject_performance = defaultdict(list)
    for score in monthly_scores:
        quiz = Quiz.query.filter_by(q_id=score.q_id).first()
        if quiz:
            subject = Subject.query.filter_by(sub_id=quiz.sub_id).first()
            if subject:
                subject_performance[subject.sub_name].append(score.total_score)
    
    # Calculate ranking (simplified - based on average score)
    all_users_avg = db.session.query(db.func.avg(Score.total_score)).filter(
        Score.time_stamp >= month_start,
        Score.time_stamp <= month_end
    ).scalar() or 0
    
    ranking = "Above Average" if average_score > all_users_avg else "Below Average"
    
    return {
        'user': user,
        'month_start': month_start,
        'month_end': month_end,
        'quiz_count': quiz_count,
        'total_score': total_score,
        'average_score': round(average_score, 2),
        'best_score': best_score,
        'worst_score': worst_score,
        'subject_performance': dict(subject_performance),
        'ranking': ranking,
        'scores': monthly_scores
    }

def send_monthly_report_email(user, report_data, month):
    """Send monthly activity report via email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['email']
        msg['To'] = user.user_mail
        msg['Subject'] = f"Quiz Master - Monthly Report for {month.strftime('%B %Y')}"
        
        # Generate HTML report
        html_report = generate_html_report(report_data, month)
        
        # Save HTML report to file
        report_filename = f"monthly_report_{user.user_id}_{month.strftime('%Y%m')}.html"
        report_filepath = os.path.join(REPORTS_DIR, report_filename)
        
        with open(report_filepath, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        # Attach HTML report
        with open(report_filepath, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {report_filename}'
            )
            msg.attach(part)
        
        # Email body
        body = f"""
        Hi {user.user_name},
        
        Your monthly activity report for {month.strftime('%B %Y')} is ready!
        
        Quick Summary:
        - Quizzes Attempted: {report_data['quiz_count']}
        - Average Score: {report_data['average_score']}%
        - Best Score: {report_data['best_score']}%
        - Performance: {report_data['ranking']}
        
        Please find the detailed HTML report attached.
        
        Keep up the great work!
        Quiz Master Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['email'], user.user_mail, text)
        server.quit()
        
    except Exception as e:
        current_app.logger.error(f"Monthly report email failed for {user.user_mail}: {e}")

def generate_html_report(report_data, month):
    """Generate HTML report"""
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Monthly Activity Report - {month.strftime('%B %Y')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
            .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat-box {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; }}
            .score-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            .score-table th, .score-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            .score-table th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Monthly Activity Report</h1>
            <h2>{report_data['user'].user_name}</h2>
            <p>{month.strftime('%B %Y')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <h3>{report_data['quiz_count']}</h3>
                <p>Quizzes Attempted</p>
            </div>
            <div class="stat-box">
                <h3>{report_data['average_score']}%</h3>
                <p>Average Score</p>
            </div>
            <div class="stat-box">
                <h3>{report_data['best_score']}%</h3>
                <p>Best Score</p>
            </div>
            <div class="stat-box">
                <h3>{report_data['ranking']}</h3>
                <p>Performance</p>
            </div>
        </div>
        
        <h3>Subject-wise Performance</h3>
        <ul>
    """
    
    for subject, scores in report_data['subject_performance'].items():
        avg_score = sum(scores) / len(scores) if scores else 0
        html_template += f"<li>{subject}: {avg_score:.1f}% (from {len(scores)} quizzes)</li>"
    
    html_template += """
        </ul>
        
        <h3>Quiz Details</h3>
        <table class="score-table">
            <tr>
                <th>Date</th>
                <th>Quiz</th>
                <th>Score</th>
            </tr>
    """
    
    for score in report_data['scores']:
        quiz = Quiz.query.filter_by(q_id=score.q_id).first()
        quiz_name = quiz.q_name if quiz else score.q_id
        html_template += f"""
            <tr>
                <td>{score.time_stamp.strftime('%Y-%m-%d')}</td>
                <td>{quiz_name}</td>
                <td>{score.total_score}%</td>
            </tr>
        """
    
    html_template += """
        </table>
    </body>
    </html>
    """
    
    return html_template