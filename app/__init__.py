from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")
    app.config['SQLALCHEMY_DATABASE_URI'] = test_config.get('DATABASE_URI') if test_config else \
        os.environ.get('DATABASE_URI', 'sqlite:///taskflow.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from . import models, routes
        db.create_all()

    return app
