import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/mydb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
