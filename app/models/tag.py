from app import db

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    
    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Tag %r>' % self.tag
