from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, g, session
from flask_login import current_user
from app import decorators
from app.models import User, Post, Comment, Tag
from slugify import slugify
from app.main.forms import CommentForm, TagForm, ProfileForm, ContactForm
from app import db
from flask_mail import Message
from app import mail


main = Blueprint('main', __name__)

def manage_prev_page():
    global session, request
    if 'profile' not in request.referrer and 'change_password' not in request.referrer \
    and 'forgot_password' not in request.referrer \
    and 'request_password'  not in request.referrer:
        session['prev_page'] = request.referrer

@main.route('/')
def homepage():
    return render_template('main/homepage.html')

@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('main/about.html')


@main.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    tags = Tag.query.all()
    return render_template('main/blog.html', posts=posts, slugify=slugify, tags=tags)


@main.route('/blog/post/<int:post_id>/<string:post_url>', methods=['GET', 'POST'])
def post(post_id, post_url):
    post = Post.query.filter_by(id=post_id).first()
    tags = Tag.query.filter_by(id=post_id)
    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date.desc())
    tags = Tag.query.filter_by(post_id=post_id)
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.content.data,
                              post_id=post_id, author_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been published')
            return redirect(url_for('main.post', post_id=post_id, post_url=post_url))
        else: 
            flash('You need to get logged in to comment')
    return render_template('main/post.html', post=post, form=form, comments=comments, tags=tags, post_id=post_id, post_url=post_url )

@main.route('/profile', methods=['GET', 'POST'])
@decorators.login_required
def profile():
    if request.method == 'GET':
        manage_prev_page()
    form = ProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been changed!')
            return redirect(session['prev_page'])
        else:
            flash('Please check your data!')
    return render_template('main/profile.html', form=form)



    



        