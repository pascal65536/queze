from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Таблица пользователей
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    level = db.Column(
        db.String(50), nullable=False, default="user"
    )  # Поле для уровня доступа

    def __repr__(self):
        return f"<User {self.username}>"

    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False


# Таблица результатов тестов
class Result(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Result {self.name}>"


dashboard_results = db.Table(
    'dashboard_results',
    db.Column('dashboard_id', db.Integer, db.ForeignKey('dashboard.id'), primary_key=True),
    db.Column('result_id', db.Integer, db.ForeignKey('results.id'), primary_key=True)
)

class Dashboard(db.Model):
    __tablename__ = 'dashboard'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    selected_theme = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    results = db.relationship('Result', secondary=dashboard_results, backref=db.backref('dashboards', lazy=True))
    user = db.relationship('User', backref=db.backref('dashboards', lazy=True)) 

    def __repr__(self):
        return f'<Dashboard {self.selected_theme}>'
