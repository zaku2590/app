from flask import Blueprint, render_template, request, jsonify, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import os
from app.models import db, User
main_bp = Blueprint("main", __name__)

# アップロードフォルダの設定
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main_bp.route("/", methods=["GET"])
def home_page():
    username = session.get("user")
    return render_template("home.html", user=username)

@main_bp.route("/score", methods=["GET"])
def onephrase_page():
    return render_template("score.html")

@main_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@main_bp.route("/register_input", methods=["POST"])
def register_user():
    username = request.form.get("username")
    password = request.form.get("password")

    if User.query.filter_by(username=username).first():
        return "⚠️ ユーザー名は既に使われています。<a href='/register'>戻る</a>"

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    session["user"] = username
    return redirect("/")

@main_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@main_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@main_bp.route("/login_input", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session["user"] = username
        return redirect("/")
    else:
        return "ログイン失敗！<a href='/login'>戻る</a>"

@main_bp.route("/pomodolo", methods=["GET"])
def pomodolo():
    return render_template("pomodolo.html")

# 📆 カレンダーページを表示
@main_bp.route("/progress_calendar_page", methods=["GET"])
def progress_calendar_page():
    return render_template("progress_calendar.html")