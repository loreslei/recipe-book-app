from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

bp = Blueprint('recipes', __name__, url_prefix='/recipes')


@bp.route('/', methods=['GET'])
@login_required
def home():
    return render_template('home.html')

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return 'pagina de adicionar receita'
    else:
        # TODO: adicionar receita no banco
        pass