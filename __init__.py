# __init__.py

import os
from dotenv import load_dotenv
load_dotenv()

from datetime import timedelta
from flask import Flask
from authlib.integrations.flask_client import OAuth
from app.models import db  # ✅ models.py の db をインポート

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)  # ✅ Flask app に models.py の db を登録

    app.permanent_session_lifetime = timedelta(days=365)

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

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app
