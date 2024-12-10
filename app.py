from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from models import db, User, Dashboard, Result
from forms import LoginForm
from datetime import datetime
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
        user = User.query.filter_by(
            username=form.username.data, password=form.password.data
        ).first()
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


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.level == 'admin':
        user_dashboards = Dashboard.query.join(User).all()
    else:
        user_dashboards = Dashboard.query.filter_by(user_id=current_user.id).join(User).all()
    return render_template('dashboard.html', dashboards=user_dashboards)


if __name__ == "__main__":
    app.run(debug=True)
