from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app, db
from waitress import serve

app = create_app('default')
# manager = Manager(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)