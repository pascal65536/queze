from tokenize import String

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms import SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError, EqualTo
import json
from wtforms import HiddenField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    # Добавлено поле для CSRF токена
    csrf_token = HiddenField()


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=25, message="Имя пользователя должно быть длиной от 4 до 25 символов.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Пароль должен быть длиной не менее 8 символов.")])
    # ввод классов
    link_class = TextAreaField('Link Class', validators=[
        DataRequired(),
        Length(min=1, message="Это поле не может быть пустым")])
    #  выбор роли
    role = SelectField('Role', choices=[('admin', 'admin'), ('teacher', 'teacher'), ('student', 'student')], validators=[
        DataRequired(),
        Length(min=1, message="Это поле не может быть пустым")])
    submit = SubmitField('Register')
    # Добавлено поле для CSRF токена
    csrf_token = HiddenField()

class SelectForm(FlaskForm):
    # выбор метода сортировки
    sort_method = SelectField('Sort_method', choices=[('sort-date', 'По дате'), ('sort-fio', 'По ФИО'), ('sort-percent', 'По проценту')], validators=[DataRequired()])
     # выбор класса
    school_class = SelectField('School_class', choices=[('', 'Все классы')], validators=[])
     # выбор метода сортировки
    sort = SelectField("Sort", choices=[('sort-ahead', 'Прямая сортировка'), ('sort-reverse', 'Обратная сортировка')], validators=[DataRequired()])
    search_query = StringField("Search_query", validators=[])
    submit = SubmitField("Отправить")
    # Добавлено поле для CSRF токена
    csrf_token = HiddenField()