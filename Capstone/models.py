from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(80), unique=True, nullable=False)
    password = db.Column(String(200), nullable=False)
    role = db.Column(String(10), nullable=False)  # 'User' or 'Admin'
