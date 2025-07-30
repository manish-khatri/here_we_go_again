#!/bin/bash

# Script to run Celery Beat for scheduled tasks
# This should be run in a separate terminal alongside the main Celery worker

echo "Starting Celery Beat for scheduled tasks..."
echo "Make sure Redis is running and the main Celery worker is also running"

# Activate virtual environment (Windows)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    # Linux/macOS
    source venv/bin/activate
fi

# Start Celery Beat
celery -A backend.celery_app beat --loglevel=info

echo "Celery Beat stopped"
