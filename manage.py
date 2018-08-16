from flask import Flask
import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import config
from app import create_app, db
from flask_bootstrap import Bootstrap
from app.models.post import Post


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
bootstrap = Bootstrap(app)


if __name__ == '__main__':
    manager.run()