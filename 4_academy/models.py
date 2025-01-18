from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    # Новое поле для хранения пути к изображению профиля
    profile_image = db.Column(db.String(255), nullable=True) # добавили новое поле

    def __init__(self, username, password, role='student', profile_image=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.profile_image = profile_image  # Инициализируем новое поле


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'