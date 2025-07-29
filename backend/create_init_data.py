from flask import current_app as app
from backend.models import db
from flask_security import SQLAlchemySessionUserDatastore, hash_password

with app.app_context():
    db.create_all()

    userdatastore: SQLAlchemySessionUserDatastore = app.security.datastore

    # Create roles
    admin_role = userdatastore.find_or_create_role(name='admin')
    customer_role = userdatastore.find_or_create_role(name='customer')

    # Create admin user if not exists
    if not userdatastore.find_user(email='admin@quiz.com'):
        admin_user = userdatastore.create_user(
            email='admin@quiz.com',
            user_name='admin',
            password=hash_password('admin')
        )
        userdatastore.add_role_to_user(admin_user, admin_role)

    # Create regular user if not exists
    if not userdatastore.find_user(email='user0@quiz.com'):
        user = userdatastore.create_user(
            email='user0@quiz.com',
            user_name='user',
            password=hash_password('user')
        )
        userdatastore.add_role_to_user(user, customer_role)

    db.session.commit()
