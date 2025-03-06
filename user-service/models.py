import re
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import Enum

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(Enum('admin', 'user', name='user_roles'), nullable=False, default='user')

    def set_password(self, password):
        if not self.validate_password(password):
            raise ValueError("La contraseña no cumple con los requisitos de seguridad")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def validate_username(username):
        pattern = r"^[A-Z]{4}\d{6}[A-Z]{1}[A-Z]{2}[A-Z0-9]{3}[A-Z]{2}\d{1}$"
        return re.fullmatch(pattern, username) is not None

    @staticmethod
    def validate_password(password):
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{8}$"
        return re.fullmatch(pattern, password) is not None
