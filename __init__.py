import os
from flask import Flask
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from app.models import db

def create_app():
    """Flaskアプリのインスタンスを作成して返す"""
    app = Flask(__name__)

    # 環境変数をロード
    load_dotenv()

    # アプリの設定を適用
    app.config.from_object("app.config.Config")

    # DB初期化
    db.init_app(app)

    # OAuth登録（OAuth 1.0a 用）
    oauth = OAuth(app)
    twitter = oauth.register(
        name='twitter',
        client_key=os.getenv("TWITTER_API_KEY"),      # ← 修正ポイント
        client_secret=os.getenv("TWITTER_API_SECRET"),
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authorize',
        api_base_url='https://api.twitter.com/1.1/',
    )

    # twitterオブジェクトをFlaskアプリに追加
    app.twitter = twitter

    # ルート（エンドポイント）を登録（最後）
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
