from flask import Flask
from flask_cors import CORS
from backend.config import LocalDevelopmentConfig
from backend.models import db, User, Role
from flask_security import Security, SQLAlchemySessionUserDatastore, auth_required
from backend.cache import init_cache
from backend.scheduler import init_scheduler

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)

    # Enable CORS
    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

    # Initialize Redis cache
    try:
        init_cache(app)
        app.logger.info("Redis cache initialized successfully")
    except Exception as e:
        app.logger.warning(f"Redis cache initialization failed: {e}")

    #flask_security
    datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    app.security= Security(app, datastore=datastore, register_blueprint=False)
    app.app_context().push()

    return app

app = create_app()

# Initialize Celery scheduler
try:
    from backend.celery_app import celery
    init_scheduler(celery)
    app.logger.info("Celery scheduler initialized successfully")
except Exception as e:
    app.logger.warning(f"Celery scheduler initialization failed: {e}")

import backend.create_init_data

import backend.routes

if (__name__== '__main__'):
    app.run(debug=True)