@echo off
echo Starting Celery Beat for scheduled tasks...
echo Make sure Redis is running and the main Celery worker is also running

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Celery Beat
celery -A backend.celery_app beat --loglevel=info

echo Celery Beat stopped
pause
