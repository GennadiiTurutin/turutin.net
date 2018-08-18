
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from datetime import datetime
from flask_login import  UserMixin 
import hashlib


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    date = db.Column(db.String(20), index=True, default=datetime.now().strftime('%Y-%m-%d'))
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.avatar_hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password == password

    def gravatar(self, size=60, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=self.avatar_hash, size=size, default=default, rating=rating)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


