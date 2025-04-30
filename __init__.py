# __init__.py

import os
from dotenv import load_dotenv
load_dotenv()

from datetime import timedelta
from flask import Flask
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy: 再接続設定を有効化
db = SQLAlchemy(engine_options={"pool_pre_ping": True})

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # DB初期化（再接続サポート付き）
    db.init_app(app)

    # セッションの有効期限（1年）
    app.permanent_session_lifetime = timedelta(days=365)

    # Twitter OAuth設定
    oauth = OAuth(app)
    twitter_key = os.getenv("TWITTER_API_KEY")
    twitter_secret = os.getenv("TWITTER_API_SECRET")

    twitter = oauth.register(
        name='twitter',
        client_id=twitter_key,
        client_secret=twitter_secret,
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authorize',
        api_base_url='https://api.twitter.com/1.1/',
    )
    app.twitter = twitter

    # Blueprint登録
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # リクエスト終了時にDBセッションを解放
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app
