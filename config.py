import os
basedir = os.path.abspath(os.path.dirname(__file__))
from decouple import config

import redis


class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 299
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = config('FLASKY_ADMIN')
    SSL_REDIRECT = False
    MAIL_HOST_USER = config('MAIL_HOST_USER')
    MAIL_HOST_PASSWORD = config('MAIL_HOST_PASSWORD')
    MAIL_HOST_URL = config('MAIL_HOST_URL')

    # Flask-Session
    SESSION_TYPE = 'filesystem'


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="GennadiiT",
    password=os.environ.get('database_password'),
    hostname="GennadiiT.mysql.pythonanywhere-services.com",
    databasename="GennadiiT$MyBlog",
    )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

