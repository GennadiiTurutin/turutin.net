from app import create_app, db
from waitress import serve

app = create_app('default')


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)