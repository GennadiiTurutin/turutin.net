from flask import jsonify, g, Blueprint, render_template, json, request, url_for
from flask_login import current_user
from app.models import User, Post
from app.api.errors import error_response, bad_request
from app import db


api = Blueprint('api', __name__)


@api.route('/api')
def api_view():
    return render_template('main/api.html')


@api.route('/users/<string:username>')
def get_user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['id'] = user.id
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['date'] = user.date

    return jsonify({'user' : user_data})

@api.route('/users')
def get_users():

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['date'] = user.date
        output.append(user_data)

    return jsonify({'users' : output})


@api.route('/posts/<int:id>')
def get_post(id):
    return jsonify(Post.query.get_or_404(id).json())


@api.route('/posts')
def get_posts():
    return jsonify(Post.json(Post.query))



