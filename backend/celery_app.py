from celery import Celery
from flask import Flask
from backend.config import LocalDevelopmentConfig

def make_celery(app_name=__name__):
    flask_app = Flask(app_name)
    flask_app.config.from_object(LocalDevelopmentConfig)
    celery = Celery(
        app_name,
        broker=flask_app.config['CELERY_BROKER_URL'],
        backend=flask_app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(flask_app.config)
    return celery

celery = make_celery() 