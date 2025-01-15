from flask import Flask
from models import db, User, Dashboard, Result
from datetime import datetime, timedelta
import behoof as utils
from random import choice, random, shuffle, randint


vowel = "aeiouy"  # гласные
consonant = "bcdfghjklmnpqrstvwxz"  # согласные
rus_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def generate_fake_result(length=6):
    r = random()
    alphabet = list(consonant + vowel)
    shuffle(alphabet)
    res = ""
    for ch in alphabet:
        if random() > r:
            res += ch.upper()
        else:
            res += ch.lower()
    return res[:length]


def generate_fake_class(level=9):
    if not level:
        level = choice(["7", "8", "9", "10", "11"])
    return f"{level}{choice(rus_alphabet[:5])}".upper()


def generate_fake_name(length=3):
    """
    Функция генерирует "фейковое" имя
    """
    return "".join(
        f"{choice(consonant)}{choice(vowel)}" for _ in range(length)
    ).capitalize()


def setup_database(app):
    """
    Функция для создания таблиц и наполнения базы данных тестовыми данными.
    """
    count = 250
    with app.app_context():
        db.create_all()
        if User.query.first():
            print("Таблица User уже существует. Данные не добавлены.")
            return

        password = utils.get_md5hash("11SSdd!!asdf")
        first_name = generate_fake_name()
        second_name = generate_fake_name(4)
        class_name = None
        admin = User(
            username="subscription",
            password=password,
            level="admin",
            first_name=first_name,
            second_name=second_name,
            class_name=class_name,
        )

        user_lst = [admin]
        for _ in range(count):
            password = None
            first_name = generate_fake_name()
            second_name = generate_fake_name(4)
            username = f"{first_name}_{second_name}".lower()
            class_name = generate_fake_class()
            user = User(
                username=username,
                password=password,
                level="user",
                first_name=first_name,
                second_name=second_name,
                class_name=class_name,
            )
            user_lst.append(user)

        db.session.add_all(user_lst)
        db.session.commit()

        if Result.query.first():
            print("Таблица Result уже существует. Данные не добавлены.")
            return

        name_lst = ['Анимация', 'Программирование', 'Текст', 'Видео', 'СистемыСчисления', 'СложениеВДвоичной', 'ТаблицыИстинности']
        result_lst = list()
        for _ in range(count):
            for name in name_lst:
                for ch in generate_fake_result():
                    label=ch.lower()
                    value=int(ch.isupper())
                    result = Result(name=name, label=label, value=value)
                    result_lst.append(result)

        db.session.add_all(result_lst)
        db.session.commit()

        if Dashboard.query.first():
            print("Таблица Dashboard уже существует. Данные не добавлены.")
            return

        dashboard_lst = list()
        for user in user_lst[1:]:
            results = list()
            for name in name_lst:
                results.append(result_lst.pop(0))
            rd = randint(0, 30)
            rm = randint(0, 59)
            rs = randint(0, 59)
            time_delta = timedelta(days=rd, minutes=rm, seconds=rs)
            dashboard = Dashboard(
                user_id=user.id,
                selected_theme=f"Theme {len(name) % 3}",
                date=datetime.now() - time_delta,
                results=results,
            )
            dashboard_lst.append(dashboard)
        db.session.add_all(dashboard_lst)
        db.session.commit()
        print("База данных успешно создана и наполнена тестовыми данными.")


if __name__ == "__main__":
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.run(debug=True)
    db.init_app(app)
    setup_database(app)
