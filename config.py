import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SQLALCHEMY_DATABASE_URI = "postgresql://myuser:pomolog@localhost/pomolog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
