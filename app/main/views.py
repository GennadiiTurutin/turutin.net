from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, g
from flask_login import current_user
from app import decorators
from app.models import User, Post, Comment, Tag
from slugify import slugify
from app.main.forms import CommentForm, TagForm, ProfileForm, ContactForm
from app import db
from flask_mail import Message
from app import mail


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def homepage():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message("Request from a client",
                          sender="gennadii.turutin@gmail.com",
                          recipients=["gennadii.turutin@gmail.com"])
        msg.html = render_template('email/request.html', form=form)
        mail.send(msg)
        flash('Your message has been sent.', 'success')
        return redirect(url_for('main.homepage'))
    return render_template('main/homepage.html', form=form)

@main.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    tags = Tag.query.all()
    return render_template('main/blog.html', posts=posts, slugify=slugify, tags=tags)


@main.route('/blog/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message("Request from a client",
                          sender="gennadii.turutin@gmail.com",
                          recipients=["gennadii.turutin@gmail.com"])
        msg.html = render_template('email/request.html', form=form)
        mail.send(msg)
        flash('Your message has been sent.', 'success')
        return redirect(url_for('main.blog'))
    return render_template('main/contact_me.html', form=form)

@main.route('/blog/terms')
def terms():
    return render_template('main/terms.html')

@main.route('/blog/privacy')
def privacy():
    return render_template('main/privacy.html')

@main.route('/blog/api')
def api_view():
    return render_template('main/api.html')


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
            flash('Your comment has been published.', 'success')
            return redirect(url_for('main.post', post_id=post_id, post_url=post_url))
        else: 
            flash('You need to get logged in to comment', 'info')
    return render_template('main/post.html', post=post, form=form, comments=comments, tags=tags, post_id=post_id, post_url=post_url )

@main.route('/blog/profile', methods=['GET', 'POST'])
@decorators.login_required
def profile():
    form = ProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been changed!', 'info')
            return redirect(url_for('main.blog'))
        else:
            flash('Please check your data!', 'warning')
    return render_template('main/profile.html', form=form)



    



        