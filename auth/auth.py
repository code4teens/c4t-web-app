from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
import bcrypt

from models import User

auth = Blueprint('auth', __name__, template_folder='templates/auth')


@auth.route('/login')
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('user.profile', id=current_user.id))

    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    id = request.form.get('id')
    password = request.form.get('password')
    user = User.query.filter_by(id=id).one_or_none()

    if user is None:
        flash('Invalid ID')
    else:
        if bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        ):
            login_user(user)

            return redirect(url_for('user.profile', id=current_user.id))
        else:
            flash('Invalid password')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))
