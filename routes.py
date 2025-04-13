from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import date, datetime
from app.models import db, User, Progress
from app.services import generate_response_score, get_logged_in_user

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def home_page():
    username = session.get("twitter_user") or session.get("user")
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

    session.pop("twitter_user", None)
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

    username = user_info["screen_name"]

    # ユーザーがDBに存在しない場合は新規登録する
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, password="twitter_login")  # パスワードはダミーでもOK
        db.session.add(user)
        db.session.commit()

    session.pop("user", None)
    session["twitter_user"] = username
    return redirect("/")

@main_bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("twitter_user", None)
    return redirect("/")

@main_bp.route("/login_input", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session.pop("twitter_user", None)
        session["user"] = username
        return redirect("/")
    else:
        return "ログイン失敗！<a href='/login'>戻る</a>"

@main_bp.route("/pomodolo", methods=["GET"])
def pomodolo():
    return render_template("pomodolo.html")

@main_bp.route("/calendar")
def calendar_page():
    return render_template("calendar.html")

@main_bp.route("/record_progress", methods=["POST"])
def record_progress():
    username = session.get("twitter_user") or session.get("user")
    if not username:
        return jsonify({"message": "ログインしていないため記録しません"}), 401

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
    username = session.get("twitter_user") or session.get("user")
    if not username:
        return jsonify({"count": 0})

    user = User.query.filter_by(username=username).first()
    today = date.today()
    progress = Progress.query.filter_by(user_id=user.id, date=today).first()

    return jsonify({"count": progress.count if progress else 0})

@main_bp.route("/get_progress_calendar", methods=["GET"])
def get_progress_calendar():
    username = request.args.get("username")

    if username:
        user = User.query.filter_by(username=username).first()
        if not user or not user.is_public:
            return jsonify([])
    elif "twitter_user" in session or "user" in session:
        uname = session.get("twitter_user") or session.get("user")
        user = User.query.filter_by(username=uname).first()
    else:
        return jsonify([])

    import re
    records = Progress.query.filter_by(user_id=user.id).all()
    event_list = []

    for r in records:
        title = ""
        if r.count > 0:
            title += f"{r.count}ポモ"
        if r.score_result:
            match = re.search(r"評価[:：]\s*([A-Z]{1,3})", r.score_result)
            if match:
                rank = match.group(1)
                title += f"（評価:{rank}）" if title else f"評価:{rank}"

        if title:  # ← titleがあればイベントとして追加
            event_list.append({
                "title": title,
                "start": r.date.isoformat()[:10]  # ← 必ず YYYY-MM-DD にする
            })

    return jsonify(event_list)

@main_bp.route("/get_memo", methods=["GET"])
def get_memo():
    username = request.args.get("username") or session.get("twitter_user") or session.get("user")
    if not username:
        return jsonify({"memo": "", "count": 0})

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"memo": "", "count": 0})

    date_str = request.args.get("date")
    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    progress = Progress.query.filter_by(user_id=user.id, date=target_date).first()
    return jsonify({
        "memo": progress.memo if progress else "",
        "count": progress.count if progress else 0
    })

@main_bp.route("/save_memo", methods=["POST"])
def save_memo():
    username = session.get("twitter_user") or session.get("user")
    if not username:
        return jsonify({"message": "ログインが必要です"}), 401

    data = request.json
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
    username = session.get("twitter_user") or session.get("user")
    if not username:
        return jsonify({"result": "ログインしていません。"}), 401

    user = User.query.filter_by(username=username).first()
    today = date.today()
    progress = Progress.query.filter_by(user_id=user.id, date=today).first()

    if not progress:
        return jsonify({"result": "今日はまだ記録がありません。"})

    # すでに結果が保存されていればそれを返す
    if progress.score_result:
        return jsonify({"result": progress.score_result})

    data = {
        "count": progress.count,
        "memo": progress.memo or ""
    }

    result = generate_response_score(data)

    # 採点結果を保存
    progress.score_result = result
    db.session.commit()

    return jsonify({"result": result})

@main_bp.route("/get_visibility_status", methods=["GET"])
def get_visibility_status():
    user = get_logged_in_user()
    if not user:
        return jsonify({"is_public": False})
    return jsonify({"is_public": user.is_public})

@main_bp.route("/toggle_calendar_visibility", methods=["POST"])
def toggle_calendar_visibility():
    user = get_logged_in_user()
    if not user:
        return jsonify({"message": "ログインが必要です"}), 401
    user.is_public = not user.is_public
    db.session.commit()
    return jsonify({"is_public": user.is_public})