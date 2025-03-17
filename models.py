from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # ユーザーを識別
    date = db.Column(db.Date, default=datetime.utcnow)  # 日付
    books_read = db.Column(db.Text, nullable=True)  # 読んだ本のタイトル（カンマ区切り）
    nutrition_status = db.Column(db.String(255), nullable=True)  # 栄養の進捗情報

    def __repr__(self):
        return f'<Progress user_id={self.user_id} date={self.date}>'
