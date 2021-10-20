from flask import abort, Blueprint, render_template
from flask_login import login_required
from sqlalchemy.sql.functions import current_timestamp, current_user

from models import User

user = Blueprint('user', __name__, template_folder='templates/user')


@user.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.filter_by(id=id).one_or_none()
    if user is None:
        abort(404)

    return render_template('profile.html', user=user)


@user.route('/dashboard')
@login_required
def dashboard():
    user = User.query.filter_by(name=current_user.name)
    if user is None:
        abort(404)

    return render_template('dashboard.html', user=user)


@user.route('/other_dashboard')
@login_required
def other_dashboard():
    user = User.query.filter_by(name=current_user.name)
    if user is None:
        abort(404)

    return render_template('other_dashboard.html', user=user)
