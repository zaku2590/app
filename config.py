import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/mydb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ セッション保持を強化（モバイル対応）
    SESSION_COOKIE_SECURE = True         # HTTPS通信下でのみCookieを送信
    SESSION_COOKIE_SAMESITE = "Lax"      # OAuthリダイレクト後でもセッション維持
    SESSION_COOKIE_HTTPONLY = True       # JSによるアクセスを防ぐ（セキュリティ向上）
    SESSION_COOKIE_DOMAIN = ".pomolog.net"  # サブドメイン共通Cookie（必要に応じて）
