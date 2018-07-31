from flask import current_app
from flask_login import  UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User \'%s\'>' % self.last_name()
