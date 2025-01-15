from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from sqlalchemy.sql import func
from models import db, User, Dashboard, Result, dashboard_results
from sqlalchemy import desc
from forms import LoginForm
from datetime import datetime
import behoof as utils
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(256)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = utils.get_md5hash(form.password.data)
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            flash("Авторизация выполнена успешно.")
            return redirect(url_for("dashboard"))
        else:
            flash("Неверное имя пользователя или пароль.")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы.")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    # if current_user.level == "admin":
    #     dashboards = Dashboard.query.join(User).all()
    # else:
    #     dashboards = (
    #         Dashboard.query.filter_by(user_id=current_user.id).join(User).all()
    #     )

        
    query = (
        db.session.query(
            Dashboard.date, 
            User.id.label('user_id'),  
            User.username, 
            User.first_name, 
            User.second_name,  
            User.class_name,  
            Dashboard.selected_theme,  
            func.sum(Result.value).label('total_value'),  # Сумма значений result.value
            func.count(Result.id).label('result_count'),  # Количество результатов
            func.avg(Result.value).label('average_value')  # Среднее значение result.value
        )
        .join(User, User.id == Dashboard.user_id)  # Присоединяем таблицу User
        .join(dashboard_results, dashboard_results.c.dashboard_id == Dashboard.id)  # Присоединяем таблицу dashboard_results
        .join(Result, Result.id == dashboard_results.c.result_id)  # Присоединяем таблицу Result
        .group_by(Dashboard.date, User.id, Dashboard.selected_theme)  # Группируем по дате, пользователю и теме
        .order_by(desc(Dashboard.date))  # Сортируем по дате в порядке убывания
    )
    dashboards = query.all()
    return render_template("dashboard.html", dashboards=dashboards)


if __name__ == "__main__":
    app.run(debug=True)
