import os
from flask_mail import Mail
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from elasticsearch import Elasticsearch

from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['DEBUG'] = True

    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    admin = Admin(app, template_mode='bootstrap3')
    mail.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
        
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.models.user import User 
    from app.models.post import Post 
    from app.models.comment import Comment 
    from app.models.tag import Tag 

    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Tag, db.session))
    admin.add_view(ModelView(Comment, db.session))

    return app



