from celery import Celery
from celery.schedules import crontab
from backend.tasks import send_daily_reminders, generate_monthly_reports

def setup_periodic_tasks(sender, **kwargs):
    """Setup periodic tasks"""
    
    # Daily reminders - every day at 6 PM
    sender.add_periodic_task(
        crontab(hour=18, minute=0),
        send_daily_reminders.s(),
        name='send_daily_reminders'
    )
    
    # Monthly reports - first day of every month at 9 AM
    sender.add_periodic_task(
        crontab(hour=9, minute=0, day_of_month=1),
        generate_monthly_reports.s(),
        name='generate_monthly_reports'
    )

def init_scheduler(celery_app):
    """Initialize the scheduler"""
    # Add periodic tasks
    celery_app.on_after_configure.connect(setup_periodic_tasks)
    
    return celery_app
