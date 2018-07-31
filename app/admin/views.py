from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from app import db
from ..decorators import admin_required
from app.admin.forms import EditPost, EditUser, NewPost
from app.models import User, Post

admin = Blueprint('admin', __name__)

@admin.route('/')
@admin_required
def index():
    """Admin dashboard page."""
    return render_template('admin/index.html')


@admin.route('/posts')
@admin_required
def posts():
    """View all posts."""
    posts = Post.query.all()
    return render_template('admin/posts.html', posts=posts)


@admin.route('/new-post', methods=['GET', 'POST'])
@admin_required
def new_post():
    """Create a new post."""
    form = NewPost()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            content=form.content.data,
            author=form.author.data)
        db.session.add(post)
        db.session.commit()
        flash('Post {} successfully created'.format(post.title()),
              'form-success')
    return render_template('admin/new_post.html', form=form)

@admin.route('/post/<int:post_id>/_delete')
@admin_required
def delete_post(post_id):
    """Delete a post."""
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        abort(404)
    else: 
        db.session.delete(post)
        db.session.commit()
        flash('Successfully deleted post %s.' % post.title(), 'success')
    return redirect(url_for('admin/posts.html'))

@admin.route('/post/<int:post_id>/_edit')
@admin_required
def edit_post(post_id):
    """Edit a post."""
    form = EditPostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            content=form.content.data,
            author=form.author.data)
        db.session.add(post)
        db.session.commit()
        flash('Post {} successfully edited'.format(post.title()),
              'form-success')
    return render_template('admin/posts.html', form=form)


@admin.route('/post/<int:post_id>')
@admin_required
def view_post(post_id):
    """View a post."""
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        abort(404)
    return render_template('admin/manage_post.html', post=post)


@admin.route('/users')
@admin_required
def registered_users():
    """View all registered users."""
    users = User.query.all()
    return render_template(
        'admin/registered_users.html', users=users)


@admin.route('/user/<int:user_id>')
@admin_required
def view_user(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('admin/user_profile.html', user=user)
    

@admin.route('/user/<int:user_id>/_delete')
@admin_required
def delete_user(user_id):
    """Delete a user's account."""
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('Successfully deleted user %s.' % user.full_name(), 'success')
    return redirect(url_for('admin.registered_users'))

