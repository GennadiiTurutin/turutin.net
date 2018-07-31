from datetime import timedelta
import os 
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY') or 'NADIA'


# SQLAlchemy.
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')


# User.
SEED_ADMIN_EMAIL = 'gennadii.turutin@gmail.com'
SEED_ADMIN_PASSWORD = 'NADIA'
REMEMBER_COOKIE_DURATION = timedelta(days=90)


