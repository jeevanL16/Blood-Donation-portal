import os
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

class Config:
    # === Flask Configuration ===
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # === Database Configuration ===
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
