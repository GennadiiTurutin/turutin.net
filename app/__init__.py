import os
from flask_mail import Mail
from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from config import config
from flask_session import Session
from flask_bootstrap import Bootstrap


basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
login = LoginManager()
mail = Mail()
sess = Session()

# Admin View: available only for admin
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not current_user.email == 'gennadii.turutin@gmail.com':
            return False
        return True

class MyPostView(ModelView): 
    form_widget_args = {"content": {'style': 'height: 500px;'}}


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login.init_app(app)
    mail.init_app(app)
    admin = Admin(app, template_mode='bootstrap3', index_view=MyAdminIndexView())
    sess.init_app(app)
   
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from app.models.user import User 
    from app.models.post import Post 
    from app.models.comment import Comment 
    from app.models.tag import Tag 
    
    admin.add_view(MyPostView(Post, db.session))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Tag, db.session))
    admin.add_view(ModelView(Comment, db.session))

    return app



