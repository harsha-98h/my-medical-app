from flask import Blueprint, request, jsonify
import bcrypt
import jwt
from datetime import datetime, timedelta

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

SECRET_KEY = 'your-secret-key-change-this'

users_db = {}

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Backend is running!'}), 200

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'patient')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        if email in users_db:
            return jsonify({'error': 'User already exists'}), 409
        
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        users_db[email] = {
            'password': hashed,
            'role': role,
            'created_at': str(datetime.now())
        }
        
        return jsonify({'message': 'User registered successfully', 'email': email}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if email not in users_db:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        user = users_db[email]
        if not bcrypt.checkpw(password.encode(), user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        token = jwt.encode(
            {'email': email, 'exp': datetime.utcnow() + timedelta(hours=24)},
            SECRET_KEY,
            algorithm='HS256'
        )
        
        return jsonify({'access_token': token, 'email': email}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
