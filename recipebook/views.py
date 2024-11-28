from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import User, Recipe
from .recipes import get_recipes_from_user_id, get_main_recipes
from . import db

bp = Blueprint('views', __name__)

@bp.route("/") 
@bp.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('recipes.home'))
    else:
        return render_template('landing.html', recipes=get_main_recipes())

@bp.route('/user/<int:user_id>')
def user(user_id):
    if current_user.is_authenticated and user_id == current_user.id:
        return redirect(url_for('recipes.home'))

    user = User.query.get(int(user_id))
    recipes = get_recipes_from_user_id(user_id)

    return render_template('user_view.html', user=user, recipes=recipes)

@bp.route("/landing")
def landing():
    if current_user.is_authenticated:
        return render_template('landing.html', recipes=get_main_recipes())
    return redirect('/')
