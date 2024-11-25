import datetime, os, uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, session
from flask_login import login_required, current_user
from . import db
from .models import User
from .file_upload import allowed_file
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('profile', __name__, url_prefix='/profile')
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

@bp.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        return render_template('edit_profile.html')
    elif request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        error = None
        # password change
        if old_password != '' and new_password != '':
            # if the old password provided matches the current password
            if check_password_hash(current_user.password, old_password):
                current_user.password = generate_password_hash(new_password)
                flash('Senha alterada com sucesso!')
            else:
                session.pop('_flashes', None)
                flash('Senha não corresponde', 'error')
        
        if current_user.name != new_username:
            current_user.name = new_username
            flash('Nome de usuário alterado com sucesso!')
        
        if current_user.email != new_email:
            current_user.email = new_email
            flash('Email alterado com sucesso!')

        # file handling
        file = request.files['file']
        filename = None

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            # if the recipe already has an image
            if current_user.profile_picture:
                # replace the file by assigning the same file name for the inputed file
                filename = current_user.profile_picture
            else:
                # else, then create a new filename
                filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)

            path = os.path.join("recipebook/static/uploads", filename)
            file.save(path)
            current_user.profile_picture = filename
            flash('Foto de perfil alterada com sucesso!')



        db.session.commit()
        return redirect(url_for('recipes.home'))
        #return redirect(url_for('profile.home'))
    
