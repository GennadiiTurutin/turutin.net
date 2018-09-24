from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app, db
import flask_whooshalchemy as whooshalchemy
from app.models.post import Post 

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()