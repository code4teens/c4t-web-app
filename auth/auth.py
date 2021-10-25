from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
import bcrypt

from database import db_session
from models import User

auth = Blueprint('auth', __name__, template_folder='templates/auth')


@auth.route('/login')
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for(
            'user.dashboard',
            user_id=current_user.id,
            cohort_id=current_user.enrolments[-1].cohort.id
        ))

    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    id = request.form.get('id')
    password = request.form.get('password')
    user = User.query.filter_by(id=id).one_or_none()

    if len(id) == 0 or len(password) == 0:
        flash('Do not leave any fields blank')
    elif user is None:
        flash('ID does not exist')
    elif user.password is None:
        flash('Please click first-time login')
    elif bcrypt.checkpw(
        password.encode('utf-8'), user.password.encode('utf-8')
    ):
        login_user(user)

        return redirect(url_for(
            'user.dashboard',
            user_id=current_user.id,
            cohort_id=current_user.enrolments[-1].cohort.id
        ))
    else:
        flash('Wrong password')

    return render_template('login.html')


@auth.route('/first_login')
def first_login_get():
    return render_template('first_login.html')


@auth.route('/first_login', methods=['POST'])
def first_login_post():
    id = request.form.get('id')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    user = User.query.filter_by(id=id).one_or_none()

    if len(id) == 0 or len(password) == 0 or len(confirm_password) == 0:
        flash('Do not leave any fields blank')
    elif user is None:
        flash('ID does not exist')
    elif user.password is not None:
        flash('You already set a password')
    elif password is None or confirm_password is None \
            or password != confirm_password:
        flash('Passwords do not match')
    else:
        user.password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()
        )
        db_session.merge(user)
        db_session.commit()
        login_user(user)

        return redirect(url_for(
            'user.dashboard',
            user_id=current_user.id,
            cohort_id=current_user.enrolments[-1].cohort.id
        ))

    return render_template('first_login.html')


@auth.route('/change_password')
@login_required
def change_password_get():
    return render_template('change_password.html')


@auth.route('/change_password', methods=['POST'])
@login_required
def change_password_post():
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    user = User.query.filter_by(id=current_user.id).one_or_none()

    if len(password) == 0 or len(confirm_password) == 0:
        flash('Do not leave any fields blank', 'danger')
    elif password != confirm_password:
        flash('Passwords do not match', 'danger')
    else:
        user.password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()
        )
        db_session.merge(user)
        db_session.commit()
        flash('Password successfully changed', 'success')

    return render_template('change_password.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))
