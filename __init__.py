# __init__.py

import os
from dotenv import load_dotenv
load_dotenv()

from datetime import timedelta
from flask import Flask
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy: 切断対策をすべて有効化
db = SQLAlchemy(engine_options={
    "pool_pre_ping": True,  # 接続前に死活確認（切れてたら再接続）
    "pool_recycle": 300     # 300秒ごとに再利用（Supabaseとの相性◎）
})

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # DB初期化
    db.init_app(app)

    # セッションの有効期限（365日）
    app.permanent_session_lifetime = timedelta(days=365)

    # Twitter OAuth 設定
    oauth = OAuth(app)
    twitter = oauth.register(
        name='twitter',
        client_id=os.getenv("TWITTER_API_KEY"),
        client_secret=os.getenv("TWITTER_API_SECRET"),
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authorize',
        api_base_url='https://api.twitter.com/1.1/',
    )
    app.twitter = twitter

    # Blueprint 登録
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # リクエスト終了時に DB セッションを閉じる（リーク防止）
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app
