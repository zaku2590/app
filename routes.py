from flask import Blueprint, render_template, request, jsonify, session, redirect
from werkzeug.utils import secure_filename
from app.services import generate_response_book, analyze_food, allowed_file
from app.models import db, Progress
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
    try:
        print("📥 画像アップロード処理開始")  # ✅ ログを追加

        # ファイルが送信されたか確認
        if 'food-image' not in request.files:
            print("🚨 ファイルが見つかりません")
            return jsonify({'error': 'ファイルが見つかりません'}), 400

        file = request.files['food-image']

        # ファイルが選択されているかチェック
        if file.filename == '':
            print("🚨 ファイルが選択されていません")
            return jsonify({'error': 'ファイルが選択されていません'}), 400

        # ファイルの拡張子が許可されているか確認
        if not allowed_file(file.filename):
            print("🚨 無効なファイル形式")
            return jsonify({'error': '無効なファイル形式です'}), 400

        # アップロードフォルダの設定
        UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)  # フォルダがない場合は作成

        # ファイルを保存
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 画像解析を実行
        analysis_result = analyze_food(filepath)

        # 解析結果が `None` だった場合のエラーハンドリング
        if analysis_result is None:
            print("🚨 `analyze_food()` が `None` を返しました")
            return jsonify({'error': '画像解析に失敗しました'}), 500

        # `JSON` 形式で返す (result をオブジェクトとして統一)
        return jsonify({'message': '解析完了', 'result': {'解析結果': analysis_result}})

    except Exception as e:
        print(f"🚨 サーバーエラー: {str(e)}")  # ✅ ログを追加
        return jsonify({'error': f'サーバーエラー: {str(e)}'}), 500
    
@main_bp.route("/progress_calendar", methods=["GET"])
def get_progress_calendar():
    if "user_id" not in session:
        return jsonify({"error": "ログインが必要です"}), 401

    user_id = session["user_id"]
    progress_data = Progress.query.filter_by(user_id=user_id).all()

    # カレンダー用に日付ごとの進捗をまとめる
    progress_dict = {}
    for p in progress_data:
        date_str = p.date.strftime("%Y-%m-%d")
        progress_dict[date_str] = {
            "books_read": p.books_read,
            "nutrition_status": p.nutrition_status
        }

    return jsonify(progress_dict)

# 📆 カレンダーページを表示
@main_bp.route("/progress_calendar_page", methods=["GET"])
def progress_calendar_page():
    return render_template("progress_calendar.html")