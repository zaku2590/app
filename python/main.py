from flask import Flask, redirect, render_template, request, jsonify, session
import openai
import os
import logging
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = "your_secret_key"

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI APIを使って応答を生成する関数
def generate_response(user_request):
    prompt = f"""
    ユーザーの要望:
    {user_request}
    上記の情報を元に、適切な返信を考えてください。
    """

    try:
        # OpenAI APIの最新の呼び出し方に変更
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"エラー: {str(e)}"

# ログインページ
@app.route("/", methods=["GET"])
def login_page():
    return render_template("home.html")

@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

# ログイン処理
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "password":
        session["user"] = username
        return redirect("/chat")
    else:
        return "ログイン失敗！<a href='/'>戻る</a>"

@app.route("/book", methods=["GET"])
def book():
    if "chat_history" not in session:
        session["chat_history"] = []
    return render_template("book.html", chat_history=session["chat_history"])

@app.route("/chat2", methods=["POST"])
def chat2():
    user_query = request.json.get("message", "").strip()
    if not user_query:
        return jsonify({"error": "メッセージが空です"}), 400

    ai_response = generate_response(user_query)

    session.setdefault("chat_history", []).append({"user": user_query, "ai": ai_response})
    session.modified = True

    return jsonify({"user": user_query, "ai": ai_response})

@app.route("/upload", methods=["POST"])
def upload():
    user_request = request.form.get("request", "").strip()
    if not user_request:
        return jsonify({"error": "リクエストが空です"}), 400

    ai_response = generate_response(user_request)

    session.setdefault("chat_history", []).append({"user": user_request, "ai": ai_response})
    session.modified = True

    return jsonify({"user": user_request, "ai": ai_response})

if __name__ == "__main__":
    app.run(port=8888, debug=True)
