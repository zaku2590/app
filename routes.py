from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import date, datetime
from app.models import db, User, Progress
from app.services import generate_response_score

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

@main_bp.route("/login/twitter")
def login_twitter():
    redirect_uri = url_for("main.twitter_callback", _external=True)
    return current_app.twitter.authorize_redirect(redirect_uri)

@main_bp.route("/login/callback")
def twitter_callback():
    token = current_app.twitter.authorize_access_token()
    resp = current_app.twitter.get("account/verify_credentials.json")
    user_info = resp.json()
    session["twitter_user"] = user_info["screen_name"]
    return redirect("/")

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

@main_bp.route("/record_progress", methods=["POST"])
def record_progress():
    if "user" not in session:
        return jsonify({"message": "ログインしていないため記録しません"}), 401

    username = session["user"]
    user = User.query.filter_by(username=username).first()
    today = date.today()

    progress = Progress.query.filter_by(user_id=user.id, date=today).first()
    if not progress:
        progress = Progress(user_id=user.id, date=today, count=1)
        db.session.add(progress)
    else:
        progress.count += 1

    db.session.commit()
    return jsonify({"message": "記録しました", "count": progress.count})

@main_bp.route("/get_progress_count", methods=["GET"])
def get_progress_count():
    if "user" not in session:
        return jsonify({"count": 0})

    username = session["user"]
    user = User.query.filter_by(username=username).first()
    today = date.today()
    progress = Progress.query.filter_by(user_id=user.id, date=today).first()

    return jsonify({"count": progress.count if progress else 0})

@main_bp.route("/calendar")
def calendar_page():
    return render_template("calendar.html")


@main_bp.route("/get_progress_calendar", methods=["GET"])
def get_progress_calendar():
    if "user" not in session:
        return jsonify([])

    username = session["user"]
    user = User.query.filter_by(username=username).first()
    records = Progress.query.filter_by(user_id=user.id).all()

    event_list = []
    for r in records:
        if r.count > 0:  # ✅ ポモ回数が1以上のときだけ追加
            event_list.append({
                "title": f"     {r.count}ポモ",
                "start": r.date.isoformat()
            })

    return jsonify(event_list)

@main_bp.route("/get_memo", methods=["GET"])
def get_memo():
    if "user" not in session:
        return jsonify({"memo": "", "count": 0})

    username = session["user"]
    user = User.query.filter_by(username=username).first()
    date_str = request.args.get("date")
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    progress = Progress.query.filter_by(user_id=user.id, date=target_date).first()
    return jsonify({
        "memo": progress.memo if progress else "",
        "count": progress.count if progress else 0
    })

@main_bp.route("/save_memo", methods=["POST"])
def save_memo():
    if "user" not in session:
        return jsonify({"message": "ログインが必要です"}), 401

    data = request.json
    username = session["user"]
    user = User.query.filter_by(username=username).first()
    target_date = datetime.strptime(data["date"], "%Y-%m-%d").date()

    progress = Progress.query.filter_by(user_id=user.id, date=target_date).first()
    if not progress:
        progress = Progress(user_id=user.id, date=target_date, count=0)

    progress.memo = data["memo"]
    db.session.add(progress)
    db.session.commit()

    return jsonify({"message": "保存しました！"})

@main_bp.route("/score_today", methods=["GET"])
def score_today():
    if "user" not in session:
        return jsonify({"result": "ログインしていません。"}), 401

    username = session["user"]
    user = User.query.filter_by(username=username).first()

    today = date.today()
    progress = Progress.query.filter_by(user_id=user.id, date=today).first()

    if not progress:
        return jsonify({"result": "今日はまだ記録がありません。"})

    data = {
        "count": progress.count,
        "memo": progress.memo or ""
    }

    result = generate_response_score(data)
    print("🧠 AI採点結果:", result)
    return jsonify({"result": result})
