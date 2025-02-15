from flask import Blueprint, render_template, request, jsonify, session, redirect
from werkzeug.utils import secure_filename
from app.services import generate_response_book, analyze_nutrition, allowed_file
import os
main_bp = Blueprint("main", __name__)

# アップロードフォルダの設定
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main_bp.route("/", methods=["GET"])
def login_page():
    return render_template("home.html")

@main_bp.route("/nutrition", methods=["GET"])
def nutrition_page():
    return render_template("nutrition.html")

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

@main_bp.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("message", "").strip()
    if not user_query:
        return jsonify({"error": "メッセージが空です"}), 400

    ai_response = generate_response_book(user_query)

    session.setdefault("chat_history", []).append({"user": user_query, "ai": ai_response})
    session.modified = True

    return jsonify({"user": user_query, "ai": ai_response})

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'food-image' not in request.files:
        return jsonify({'error': 'ファイルが見つかりません'}), 400
    
    file = request.files['food-image']
    if file.filename == '':
        return jsonify({'error': 'ファイルが選択されていません'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 画像解析の実行
        analysis_result = analyze_nutrition(filepath)
        
        return jsonify({'message': '解析完了', 'result': analysis_result})
    
    return jsonify({'error': '無効なファイル形式です'}), 400