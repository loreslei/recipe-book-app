from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import db
from .models import Recipe, User
import datetime

bp = Blueprint('recipes', __name__, url_prefix='/recipes')


@bp.route('/', methods=['GET'])
@login_required
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes=recipes)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('create_recipe.html')
    else:
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        category = request.form.get('category')

        current_date = datetime.datetime.now()
        new_recipe = Recipe(user_id=current_user.id, title=title, ingredients=ingredients, steps=steps, date_created=current_date, category=category)

        db.session.add(new_recipe)
        db.session.commit()

        return redirect(url_for('recipes.home'))