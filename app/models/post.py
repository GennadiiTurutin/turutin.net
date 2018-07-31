from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    subtitle = db.Column(db.Text)
    content = db.Column(db.Text)
    author = db.Column(db.Text)



