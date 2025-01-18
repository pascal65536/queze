from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash,
    abort,
    make_response,
    session
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from sqlalchemy.testing.suite.test_reflection import users
import hashlib
from login_form import LoginForm, RegistrationForm, SelectForm
from Utils.Utils import get_send_data, search_students, get_admin_send_data
import os
import json
import secrets

import csv
from io import StringIO

import os  
import mimetypes  
from flask import send_from_directory

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

def generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_hex(16)
    return session["_csrf_token"]


app.jinja_env.globals["csrf_token"] = generate_csrf_token

# Путь к папке для загрузок относительно директории скрипта
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Проверяем, существует ли папка загрузок, если нет - создаём её
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# Сохраняем путь к папке загрузок в конфигурацию Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Маршрут для обслуживания загруженных файлов,
# <path:filename> -  указывает на то, что переменная 'filename' может содержать '/'
@app.route("/uploads/<path:filename>")
def uploads_folder(filename):
    """
    Отправляет статический файл из папки загрузок.
    :param filename: Имя файла, который нужно отправить.
    """
    # send_from_directory() - отправляет файл из указанной папки
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

#Класс пользователя, в дальнейшем в него записываются данные из файла

class Student(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

class User(UserMixin):
    def __init__(self, id, username, password, role, link_class):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.link_class = link_class
    def __repr__(self):
        return f'{self.id} {self.username} {self.password}'

def read_json_users_data(json_name):
    """
    Считывание json файла с данными
    :param json_name: название json
    :return: словарь с данными пользователей
    """
    with open(json_name, "r", encoding="UTF-8") as file:
        json_dict = json.load(file)
        users = {int(user_id): User(user_id, json_dict[user_id]["username"], json_dict[user_id]["password"],
                                    json_dict[user_id]["role"], json_dict[user_id]["link_class"]) for user_id
                 in json_dict.keys()}
        return users
    
def read_json(json_name):
    """
    Считывание json файла с данными
    :param json_name: название json
    :return: словарь с данными
    """
    with open(json_name, "r", encoding="UTF-8") as file:
        json_dict = json.load(file)
        return json_dict

@login_manager.user_loader
def load_user(user_id):
    users = read_json_users_data("Users_login_info.json")
    return users.get(int(user_id))

@app.route('/', methods=["POST", "GET"])
@login_required
def index():
    return redirect("/result")

@app.route("/result", methods=['GET', 'POST'])
@login_required
def result():
    form = SelectForm()
    user = current_user._get_current_object()
    data = read_json("Users_login_data.json")
    sort_method = form.sort_method.data
    school_class = form.school_class.data
    sort_param = form.sort.data
    search_query = form.search_query.data
    
    # Проверяем, был ли отправлен POST запрос и есть ли файл с именем 'profile_image'
    if request.method == 'POST' and 'profile_image' in request.files:
            # Получаем файл из запроса
            file = request.files['profile_image']
            # Проверяем, что файл существует и у него есть имя
            if file and file.filename != '':
                # Получаем MIME-тип файла
                mime_type, _ = mimetypes.guess_type(file.filename)
                # Проверяем, что MIME-тип файла является изображением
                if mime_type and mime_type.startswith('image/'):
                    # Формируем полный путь для сохранения файла
                    file_save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(file_save_path)
                    # Обновляем поле profile_image в данных пользователя
                    user_id = str(user.id) # получаем id пользователя
                    users = read_json_users_data("Users_login_info.json") # считываем файл с данными пользователя

                    with open("Users_login_info.json", "r", encoding="utf-8") as f: # Открываем для чтения
                        users_dict = json.load(f) # получаем словарь

                    users_dict[user_id]["profile_image"] = f'/uploads/{file.filename}' # Добавляем данные о пути к картинке в словарь
                    with open("Users_login_info.json", 'w', encoding='UTF-8') as f: # Записываем изменения
                       json.dump(users_dict, f, ensure_ascii=False, indent=5)

                    flash('Изображение профиля успешно загружено!', 'success')
                else:
                     flash('Можно загружать только изображения!', 'error')
    
    if user.role == "teacher":
        link_class = sorted(user.link_class)
        send_data = get_send_data(link_class, data, sort_method, school_class, sort_param)
        send_data = search_students(send_data, search_query)
        session['data'] = send_data
        return render_template("result.html", classes=send_data, form=form, link_classes=link_class)
    elif user.role == "admin":
        send_data = get_admin_send_data(data, sort_method, school_class, sort_param)
        link_class = sorted(send_data.keys())
        send_data = search_students(send_data, search_query)
        
        session['data'] = send_data
        return render_template("result.html", classes=send_data, form=form, link_classes=link_class)
    else:
        link_class = user.link_class
        username = user.username
        proverka = {}
        send_data = get_send_data(link_class, data, sort_method, school_class, sort_param)
        if len(send_data) > 0:
            student_results = {}
            for key, tests in data.items():
                if user.username in key:
                    student_results[key] = tests
                    student_results = get_send_data(link_class, student_results, sort_method, school_class, sort_param)
            session['data'] = student_results
            return render_template("result.html", classes=student_results, form=form, link_classes=link_class)
        return render_template("result.html", classes=send_data, form=form, link_classes=link_class)

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    user = current_user._get_current_object()
    if user.role != "admin":
        return redirect("/")
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            passwd = form.password.data.encode('utf-8')
            password = hashlib.md5(passwd).hexdigest()
            role = form.role.data
            link_class = form.link_class.data.split(" ")
            new_user = {
                "username": form.username.data,
                "password": password,
                "role": role,
                "link_class": link_class
            }
            flash("Регистрация прошла успешно. Теперь вы можете войти.")

            with open("Users_login_info.json", "r", encoding="utf-8") as f:
                users_dict = json.load(f)
            users_dict[len(users_dict) + 1] = new_user
            with open("Users_login_info.json", 'w', encoding='UTF-8') as f:
                json.dump(users_dict, f, ensure_ascii=False, indent=5)
            return redirect(url_for("register"))
        else:
            print(form.errors)
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"]) # Логин пользователя | Предусмотреть реализацию ролей (-)
def login():
    form = LoginForm()
    users = read_json_users_data("Users_login_info.json")  # Здесь считывается файл с данными пользователей (логин, пароль, роль, классы).
    if request.method == "POST" and form.validate_on_submit():
                # Считываем вводимые данные на сайте
                username = form.username.data
                passwd = hashlib.md5(form.password.data.encode()).hexdigest()
                # Идет сравнивание хэшированного пароля и имени пользователя
                for user in users.values():
                    if user.username == username and user.password == passwd:
                        login_user(user)
                        flash('Авторизация выполнена успешно.')
                        now_user = current_user._get_current_object()
                        if now_user.role == "student":
                            return redirect("/result")
                        return redirect("/result")
                flash('Неверное имя пользователя или пароль.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/get_data", methods=["GET"])
def get_data():
    if request.method == "GET":
        name = request.args.get(
            "first_name") + f" {request.args.get("last_name")}" + f"_{request.args.get("class_name")}"
        date = request.args.get("date")
        exam_type = request.args.get("selected_theme")
        themes = {theme.split("_")[0]: theme.split("_")[1] for theme in request.args.get("mashup").split("|")}
        answers = "".join(themes.values())
        percentage = round((len([i for i in answers if i.isupper()]) / len(answers) * 100), 2)

        with open("Users_login_data.json", "r", encoding="UTF-8") as file:
            new_note = json.load(file)
        _sametest = False  # Проверка на совпадение данных в json
        _renote = False # Проверка на замену записи (что-то вроде пересдачи, если отличается хотя б 1 из ответов)

        # ------------------------------------------------------------ ОПТИМИЗИРОВАТЬ /

        if name in new_note.keys():
            for _name, _exam_type in new_note.items():
                if name == _name:
                    for records in _exam_type.values():
                        for record in records:
                            if date == record["Дата"]:
                                _sametest = True
                                break

        if _sametest:
            return render_template("error.html")
        else:
            new_note.setdefault(name, {}).setdefault(f"{exam_type}", []).append({"Дата": date, **themes ,"Правильные ответы": percentage})
            with open("Users_login_data.json", "w", encoding="UTF-8") as file:
                json.dump(new_note, file, ensure_ascii=False, indent=5)

            return render_template("info.html")

# ------------------------------------------------------------ ОПТИМИЗИРОВАТЬ \

@app.route("/download", methods=['GET', 'POST'])
@login_required
def download_csv():
    """Создание и отправка CSV файла на скачивание."""

    download_data = session.get('data')
    print(download_data)

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)

    # Записываем заголовок
    csv_writer.writerow(["Класс", "Имя ученика", "Вид теста", "Дата", "Правильные ответы"])

    for class_name, class_data in download_data.items():
        for student_name, tests in class_data.items():
            for test in tests:
                csv_writer.writerow([
                    class_name,
                    student_name,
                    test["Вид теста"],
                    test["Дата"],
                    test["Правильные ответы"]
                ])

    response = make_response(csv_buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=Results.csv'
    response.headers['Content-type'] = 'text/csv'

    return response

if __name__ == '__main__':
    app.run(debug=True)