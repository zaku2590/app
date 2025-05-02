import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/mydb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ セッション設定（スマホTwitterログイン対策）
    SESSION_COOKIE_SECURE = True               # HTTPS通信必須（Cloud RunはOK）
    SESSION_COOKIE_SAMESITE = "Lax"            # OAuthリダイレクトに必要
    SESSION_COOKIE_HTTPONLY = True             # JSからアクセス不可
    SESSION_COOKIE_NAME = "session"            # 明示的に設定（推奨）
    SESSION_COOKIE_DOMAIN = ".pomolog.net"     # ✅ 必須（ドメイン固定でセッション維持）
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)
