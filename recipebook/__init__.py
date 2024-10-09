from flask import Flask
from os import path
from flask_login import LoginManager
from .init_db import init_db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .models import User, Recipe
    init_db(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app

