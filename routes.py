from flask import Blueprint, render_template, request, jsonify, session, redirect
from werkzeug.utils import secure_filename
import os
main_bp = Blueprint("main", __name__)

# アップロードフォルダの設定
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main_bp.route("/", methods=["GET"])
def home_page():
    return render_template("home.html")

@main_bp.route("/nutrition", methods=["GET"])
def nutrition_page():
    return render_template("nutrition.html")

@main_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@main_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@main_bp.route("/login_input", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "password":
        session["user"] = username
        return redirect("/home")
    else:
        return "ログイン失敗！<a href='/'>戻る</a>"

@main_bp.route("/pomodolo", methods=["GET"])
def pomodolo():
    return render_template("pomodolo.html")

# 📆 カレンダーページを表示
@main_bp.route("/progress_calendar_page", methods=["GET"])
def progress_calendar_page():
    return render_template("progress_calendar.html")