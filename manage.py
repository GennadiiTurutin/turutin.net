from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app, db
# from gevent.pywsgi import WSGIServer
from waitress import serve

app = create_app('default')
# manager = Manager(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # manager.run()
    print('Starting')
    #app.run(host='0.0.0.0')
    serve(app, host="0.0.0.0", port=5000)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()