from flask import abort, Blueprint, render_template
from flask_login import current_user, login_required

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
    return render_template('dashboard.html', user=current_user)


@user.route('/discussions')
@login_required
def discussions():
    return render_template('discussion.html')
