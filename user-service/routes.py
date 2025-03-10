from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.json

  if User.query.filter_by(username=data['username']).first():
    return jsonify({"error": "El usuario ya está en uso"}), 400

  if User.query.filter_by(email=data['email']).first():
    return jsonify({"error": "El email ya está registrado"}), 400

  new_user = User(username=data['username'], email=data['email'], role='user')
  new_user.set_password(data['password'])
  db.session.add(new_user)
  db.session.commit()

  return jsonify({"message": "Usuario registrado exitosamente"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.json
  user = User.query.filter_by(username=data['username']).first()
  if not user or not user.check_password(data['password']):
    return jsonify({"error": "Credenciales inválidas"}), 401

  access_token = create_access_token(identity={
    'id': user.id,
    'username': user.username,
    'role': user.role
  })
  return jsonify({"access_token": access_token}), 200
