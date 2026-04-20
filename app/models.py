# models.py also needs the shared database
from flask_sqlalchemy import SQLAlchemy

# app gets connected in __initi__ so it is not needed here
# SQLAlchemy(app) -> SQAlchemy()
db = SQLAlchemy()

# User model 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="employee")