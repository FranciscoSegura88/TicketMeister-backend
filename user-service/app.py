from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'tu_clave_secreta'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(10), default='user')

@app.before_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(nombre=data['nombre'], apellido=data['apellido'], correo=data['correo'], password=hashed_password, rol=data.get('rol', 'user'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario registrado exitosamente'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(correo=data['correo']).first()

    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({'nombre': user.nombre, 'apellido': user.apellido, 'correo': user.correo, 'rol': user.rol, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Credenciales inválidas'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
