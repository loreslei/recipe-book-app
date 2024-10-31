from flask import Flask, render_template, url_for
from os import path
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(render_as_batch=True)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    from .models import User, Recipe, likes
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    with app.app_context():
        db.create_all()
        print("Database tables created!")

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(404)
    def not_found(e):
        return f'<div style="text-align: center;"><p>404</p><img width="80%" src="{url_for("static", filename="/image/404.png")}"></div>'

    from . import auth
    app.register_blueprint(auth.bp)
    from . import views
    app.register_blueprint(views.bp)
    from . import recipes
    app.register_blueprint(recipes.bp)

    return app

