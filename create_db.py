from flask import Flask
from models import db, User, Dashboard, Result
from datetime import datetime


def setup_database(app):
    """
    Функция для создания таблиц и наполнения базы данных тестовыми данными.
    """
    with app.app_context():
        db.create_all()
        if not User.query.first():
            user1 = User(username="user1", password="password1", level="user")
            user2 = User(username="user2", password="password2", level="user")
            user3 = User(username="subscription", password="11SSdd!!asdf", level="admin")
            db.session.add_all([user1, user2, user3])
            db.session.commit()

            result1 = Result(name="Result 1")
            result2 = Result(name="Result 2")
            result3 = Result(name="Result 3")
            db.session.add_all([result1, result2, result3])
            db.session.commit()

            dashboard1 = Dashboard(
                user_id=user1.id,
                selected_theme="Theme 1",
                date=datetime.now(),
                results=[result1, result2],
            )
            dashboard2 = Dashboard(
                user_id=user2.id,
                selected_theme="Theme 1",
                date=datetime.now(),
                results=[result1],
            )
            dashboard3 = Dashboard(
                user_id=user3.id,
                selected_theme="Theme 1",
                date=datetime.now(),
                results=[result2, result3],
            )
            db.session.add_all([dashboard1, dashboard2, dashboard3])
            db.session.commit()

            print("База данных успешно создана и наполнена тестовыми данными.")
        else:
            print("Таблицы уже существуют. Данные не добавлены.")


if __name__ == "__main__":
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.run(debug=True)
    db.init_app(app)
    setup_database(app)
