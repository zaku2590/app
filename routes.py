from flask import Blueprint, render_template, request, jsonify, session, redirect
from app.services import generate_response

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def login_page():
    return render_template("home.html")

@main_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@main_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "password":
        session["user"] = username
        return redirect("/book")
    else:
        return "ログイン失敗！<a href='/'>戻る</a>"

@main_bp.route("/book", methods=["GET"])
def book():
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("book.html", chat_history=session["chat_history"])

@main_bp.route("/chat2", methods=["POST"])
def chat2():
    user_query = request.json.get("message", "").strip()
    if not user_query:
        return jsonify({"error": "メッセージが空です"}), 400

    ai_response = generate_response(user_query)

    session.setdefault("chat_history", []).append({"user": user_query, "ai": ai_response})
    session.modified = True

    return jsonify({"user": user_query, "ai": ai_response})
