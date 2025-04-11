# __init__.py

import os
from dotenv import load_dotenv
load_dotenv()  # ← 必ず一番最初に呼び出す！

from flask import Flask
from authlib.integrations.flask_client import OAuth
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    db.init_app(app)

    # Twitter OAuth設定
    oauth = OAuth(app)

    # 環境変数から取得（ここでNoneにならないようにする）
    twitter_key = os.getenv("TWITTER_API_KEY")
    twitter_secret = os.getenv("TWITTER_API_SECRET")

    twitter = oauth.register(
        name='twitter',
        client_id=twitter_key,               # ← None じゃないかチェック
        client_secret=twitter_secret,
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authorize',
        api_base_url='https://api.twitter.com/1.1/',
    )

    app.twitter = twitter

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
