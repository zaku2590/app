from flask import Flask
from dotenv import load_dotenv
import os
from app.models import db

def create_app():
    """Flaskアプリのインスタンスを作成して返す"""
    app = Flask(__name__)

    # 環境変数をロード
    load_dotenv()

    # アプリの設定を適用
    app.config.from_object("app.config.Config")
    
    db.init_app(app)  # db接続

    # ルート（エンドポイント）を登録
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
