import datetime, os, uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from . import db
from .models import Recipe, User, Category
from werkzeug.utils import secure_filename
from .file_upload import allowed_file


bp = Blueprint('recipes', __name__, url_prefix='/recipes')

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def get_recipes_with_category():
    query = (
        db.session.query(
            Recipe.id,
            Recipe.user_id,
            Recipe.title,
            Recipe.ingredients,
            Recipe.steps,
            Recipe.date_created,
            Recipe.image_path,
            Category.name.label("category_name")
        )
        .filter_by(user_id=current_user.id)
        .join(Category, Recipe.category_id == Category.id)
    )
    recipes = query.all()
    return recipes

def get_recipe_by_id(recipe_id):
    query = (
        db.session.query(
            Recipe.id,
            Recipe.user_id,
            Recipe.title,
            Recipe.ingredients,
            Recipe.steps,
            Recipe.date_created,
            Recipe.image_path,
            Category.name.label("category_name"),
            User.name.label("author")
        )
        .filter_by(id=recipe_id)
        .join(User, User.id == Recipe.user_id)
        .join(Category, Recipe.category_id == Category.id)
    )
    recipe = query.first()
    return recipe

@bp.route('/', methods=['GET'])
@login_required
def home():

    recipes = get_recipes_with_category()
    
    return render_template('home.html', recipes=recipes)


@bp.route('/view/<int:recipe_id>', methods=['GET'])
# TODO: if user is logged in add some stuff
def view(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    print(recipe.image_path)
    if recipe == None:
        return abort(404)
    return render_template('comida.html', recipe=recipe)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('create_recipe.html', categories=categories)
    else:
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        category_id = request.form.get('category')
        file = request.files['file']

        filename = None

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            # TODO: add UUID to the file names to prevent duplication
            filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
            path = os.path.join("recipebook/static/uploads", filename)
            file.save(path)

        current_date = datetime.datetime.now()
        new_recipe = Recipe(
            user_id=current_user.id, 
            title=title, 
            ingredients=ingredients, 
            steps=steps, 
            date_created=current_date, 
            category_id=category_id,
            image_path=filename
        )

        db.session.add(new_recipe)
        db.session.commit()

        return redirect(url_for('recipes.home'))

@bp.route('/update/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    categories = Category.query.all()
    if recipe.user_id != current_user.id:
        return abort(404)
    if request.method == 'GET':
        return render_template('edit_recipe.html', recipe=recipe, categories=categories)
    elif request.method == 'POST':
        
        recipe.title = request.form.get('title')
        recipe.ingredients = request.form.get('ingredients')
        recipe.steps = request.form.get('steps')
        recipe.category_id = request.form.get('category')

        # file handling
        file = request.files['file']
        filename = None

        print(file)

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            # if the recipe already has an image
            if recipe.image_path:
                # replace the file by assigning the same file name for the inputed file
                filename = recipe.image_path
            else:
                # else, then create a new filename
                filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)

            path = os.path.join("recipebook/static/uploads", filename)
            file.save(path)
            recipe.image_path = filename



        db.session.commit()
        return redirect(url_for('recipes.home'))

@bp.route('/delete/<int:recipe_id>', methods=['GET'])
@login_required
def delete(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe.user_id != current_user.id:
        return abort(404)
    if request.method == 'GET':
        if recipe.image_path != None:
            os.remove(f'recipebook/static/uploads/{recipe.image_path}')
        db.session.delete(recipe)
        db.session.commit()
        return redirect(url_for('recipes.home'))


@bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    print(keyword)
    query = (
        db.session.query(
            Recipe.id,
            Recipe.user_id,
            Recipe.title,
            Recipe.ingredients,
            Recipe.steps,
            Recipe.date_created,
            Recipe.image_path,
            Category.name.label("category_name"),
            User.name.label("author")
        )
        .filter(Recipe.title.like(f"{keyword}%"))
        .join(User, User.id == Recipe.user_id)
        .join(Category, Recipe.category_id == Category.id)
    )
    
    return render_template('search.html', recipes=query.all())