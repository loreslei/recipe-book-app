from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db

bp = Blueprint('auth', __name__)    

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        error = None

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Login bem sucedido!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                error = 'Senha incorreta.'
        else:
            error = 'Email não corresponde.'
        
        
        flash(error, category='error')
        redirect('/')


    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_repeat = request.form.get('password_repeat')

        error = None

        email_exists = User.query.filter_by(email=email).first()

        if not username or not email or not password:
            error = 'Por favor preencha os campos!'
        elif email_exists:
            error = "O Email já está em uso!"
        elif password != password_repeat:
            error = "As senhas não condizem"
        
        if error is None:
            new_user = User(name=username, email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            return redirect('/')
        
        
        flash(error, category='error')


    return render_template('register.html')

@bp.route('/logout', strict_slashes=False)
@login_required
def logout():
    logout_user()
    return 'logout'