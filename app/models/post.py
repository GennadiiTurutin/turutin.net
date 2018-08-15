from app import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['title', 'subtitle', 'content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    subtitle = db.Column(db.Text)
    content = db.Column(db.Text)
    date = db.Column(db.String, index=True, default=datetime.now().strftime('%Y-%m-%d'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Post %r>' % self.title



