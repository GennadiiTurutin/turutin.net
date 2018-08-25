from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app, db
from flask_bootstrap import Bootstrap

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
bootstrap = Bootstrap(app)

if __name__ == '__main__':
    manager.run()