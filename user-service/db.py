from flask import Flask
from models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    print('Database created')
    