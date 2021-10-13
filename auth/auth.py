from flask import Blueprint, flash, render_template, request

from models import User

auth = Blueprint('auth', __name__, template_folder='templates/auth')


@auth.route('/login')
def login_get():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    id = request.form.get('id')
    password = request.form.get('password')
    user = User.query.filter_by(id=id).one_or_none()

    if user is None:
        flash('Invalid ID.')
    else:
        flash(id)

    return render_template('login.html')
