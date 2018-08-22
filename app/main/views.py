from flask import Blueprint, render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user
from app import decorators
from app.models import User, Post, Comment, Tag
from slugify import slugify
from app.main.forms import CommentForm, TagForm, SearchForm, ProfileForm
from app import db

main = Blueprint('main', __name__)

@main.before_request
def before_request():
    g.search_form = SearchForm()

@main.route('/')
def homepage():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=2)
    return render_template('main/homepage.html', posts=posts, slugify=slugify)

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/search')
def search():
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.query.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.homepage', q=g.search_form.query.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.homepage', q=g.search_form.query.data, page=page - 1) \
        if page > 1 else None
    return render_template('main/homepage.html', title=('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)

@main.route('/post/<int:post_id>/<string:post_url>', methods=['GET', 'POST'])
def post(post_id, post_url):
    post = Post.query.filter_by(id=post_id).first()
    tags = Tag.query.filter_by(id=post_id)
    form = CommentForm()
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date.desc())
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

@main.route('/profile', methods=['GET', 'POST'])
@decorators.login_required
def profile():
    form = ProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been changed!', 'info')
            return redirect(url_for('main.homepage'))
        else:
            flash('Please check your data!', 'warning')
    return render_template('main/profile.html', form=form)

    



        