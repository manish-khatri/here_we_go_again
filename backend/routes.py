from flask import current_app as app, jsonify, request
from flask_security import auth_required, verify_password, hash_password
from backend.models import db

datastore = app.security.datastore

@app.get('/')
def home():
    return 'HII'

@app.get('/protected')
@auth_required()
def protected():
    return '<h1> only accessible when authenticated </h1>'

@app.route('/login', methods=['POST'])
def login():
    data =request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    print("stage1")
    user = datastore.find_user(email=email)
    print(user.roles)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if verify_password(password, user.password):
        return jsonify({'token': user.get_auth_token(), 'email': user.email, 'role': user.roles[0].name, 'id': user.id}), 200
    else:
        return jsonify({'message': 'Invalid password'}), 400
    
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    role = data.get('role')
    password = data.get('password')

    if not email or not password or not name or role not in ['admin', 'customer']:
        return jsonify({'error': 'invalid entry'}), 400

    if datastore.find_user(email=email):
        return jsonify({'error': 'User already exists'}), 400

    try:
        datastore.create_user(email=email, user_name=name, password=hash_password(password), roles=[role], active=True)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {e}")
        return jsonify({'error': 'Failed to register user'}), 400