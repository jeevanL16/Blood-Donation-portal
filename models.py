from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class Donor(db.Model):
    __tablename__ = 'donor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    contact = db.Column(db.String(15))
    location = db.Column(db.String(100))
    approved = db.Column(db.Boolean, default=False)

class Blood_Request(db.Model):
    __tablename__ = 'blood_request'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    bloodgroup = db.Column(db.String(5))
    location = db.Column(db.String(100))
    contact = db.Column(db.String(15))
    reason = db.Column(db.String(200))
    hospital = db.Column(db.String(100))

class Contact(db.Model):
    __tablename__ = 'contact'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    message = db.Column(db.Text, nullable=False)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    message = db.Column(db.Text)
    approved = db.Column(db.Boolean, default=False)

   

