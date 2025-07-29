from flask import current_app as app
from backend.models import db
from flask_security import SQLAlchemySessionUserDatastore, hash_password

with app.app_context():
    db.create_all()

    userdatastore: SQLAlchemySessionUserDatastore = app.security.datastore

    # Create roles
    userdatastore.find_or_create_role(id='1', name='admin')
    userdatastore.find_or_create_role(id='2', name='customer')

    # Create admin user and assign role
    if not userdatastore.find_user(email='admin@quiz.com'):
        admin_user = userdatastore.create_user(
            id='A0',
            email='admin@quiz.com',
            user_name='admin',
            password=hash_password('admin'),
            fs_uniquifier='admin-uniq'
        )
        userdatastore.add_role_to_user(admin_user, 'admin')
    else:
        admin_user = userdatastore.find_user(email='admin@quiz.com')
        userdatastore.add_role_to_user(admin_user, 'admin')

    # Create customer user and assign role
    if not userdatastore.find_user(email='user0@quiz.com'):
        customer_user = userdatastore.create_user(
            id='C0',
            email='user0@quiz.com',
            user_name='user',
            password=hash_password('user'),
            fs_uniquifier='user-uniq'
        )
        userdatastore.add_role_to_user(customer_user, 'customer')
    else:
        customer_user = userdatastore.find_user(email='user0@quiz.com')
        userdatastore.add_role_to_user(customer_user, 'customer')

    db.session.commit()
