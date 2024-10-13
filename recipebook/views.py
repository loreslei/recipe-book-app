from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

bp = Blueprint('views', __name__)

@bp.route("/") 
@bp.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('recipes.home'))
    else:
        return render_template('landing.html')
