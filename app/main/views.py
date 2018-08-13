from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from app.models import User, Post, Comment, Tag
from slugify import slugify
from app.main.forms import CommentForm, TagForm
from app import db


main = Blueprint('main', __name__)


@main.route('/')
def homepage():
    posts = Post.query.all()
    return render_template('main/homepage.html', posts=posts, slugify=slugify)

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/post/<int:post_id>/<string:post_url>', methods=['GET', 'POST'])
def post(post_id, post_url):
    post = Post.query.filter_by(id=post_id).first()
    tags = Tag.query.filter_by(id=post_id)
    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post_id)
    if form.validate_on_submit():
        comment = Comment(content=form.content.data,
                          post_id=post_id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('main.post', post_id=post_id, post_url=post_url))
    return render_template('main/post.html', post=post, form=form, comments=comments, tags=tags)
