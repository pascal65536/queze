from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from sqlalchemy import desc
from sqlalchemy.sql import func
from models import db, User, Dashboard, Result, dashboard_results
import os


app = Flask(__name__)
# app.config["SECRET_KEY"] = os.urandom(256)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

session = db.session
app.app_context().push()

# import ipdb; ipdb.sset_trace()


query = (
    db.session.query(
        Dashboard.date,
        Dashboard.user_id,
        Dashboard.selected_theme,
        func.sum(Result.value).label("total_value"),
        func.count(Result.id).label("result_count"),
        func.avg(Result.value).label("average_value"),
    )
    .join(dashboard_results, dashboard_results.c.dashboard_id == Dashboard.id)
    .join(Result, Result.id == dashboard_results.c.result_id)
    .group_by(Dashboard.date, Dashboard.user_id, Dashboard.selected_theme)
)

# Выполнение запроса и получение результатов
results = query.all()

# Вывод результатов
for result in results:
    print(result.date, result.user_id, result.selected_theme, result.total_value, result.result_count, result.average_value)
