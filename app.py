from flask import Flask
from flask_cors import CORS
from backend.config import LocalDevelopmentConfig
from backend.models import db, User, Role
from flask_security import Security, SQLAlchemySessionUserDatastore, auth_required

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)

    # Enable CORS
    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])

    #flask_security
    datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    app.security= Security(app, datastore=datastore, register_blueprint=False)
    app.app_context().push()

    return app

app = create_app()

import backend.create_init_data

import backend.routes

if (__name__== '__main__'):
    app.run()