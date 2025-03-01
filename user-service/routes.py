from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return "Ya jala jijuesushingadamoder!"

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    
    new_user = User(
        name=data['name'],
        lastname=data['lastname'],
        email=data['email'],
        role='user' #Por defecto te asigna el rol de usuario
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Si se hizo tu fokin usuario alv"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity={
        'id': user.id,
        'name': user.name,
        'lastname': user.lastname,
        'role': user.role
    })
    return jsonify({"access_token": access_token}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    return jsonify({
        'id': user.id,
        'name': user.name,
        'lastname': user.lastname,
        'email': user.email,
        'role': user.role
    }), 200