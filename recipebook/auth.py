from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, logout_user

bp = Blueprint('auth', __name__)

@bp.route('/login')
def login():
    return render_template('base.html')

@bp.route('/register')
def register():
    return 'register page'

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logout'