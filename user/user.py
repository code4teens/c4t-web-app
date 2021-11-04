from datetime import datetime, timedelta
from functools import wraps

from flask import abort, Blueprint, render_template, request
from flask_login import current_user, login_required

from database import db_session
from models import Cohort, Eval, User
from utils import tz

user = Blueprint('user', __name__, template_folder='templates/user')


def admin_only(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        elif not current_user.is_admin:
            abort(403)
        else:
            return func(*args, **kwargs)

    return decorated_view


def admin_or_owner_only(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        elif not current_user.is_admin \
                and kwargs.get('user_id') != current_user.id:
            abort(403)
        else:
            return func(*args, **kwargs)

    return decorated_view


@user.add_app_template_filter
def is_past(date, day):
    today = datetime.now(tz).date()

    if today >= date + timedelta(days=day):
        return True

    return False


@user.route('/admin')
@admin_only
def admin():
    evals = Eval.query.all()

    return render_template('admin.html', evals=evals)


@user.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.filter_by(id=id).one_or_none()

    if user is None:
        abort(404)

    return render_template('profile.html', user=user)


@user.route('/dashboard/<int:user_id>/<int:cohort_id>')
@admin_or_owner_only
def dashboard(user_id, cohort_id):
    user = User.query.filter_by(id=user_id).one_or_none()
    cohort = Cohort.query.filter_by(id=cohort_id).one_or_none()

    if user is None or cohort is None or cohort.id not in [
        enrolment.cohort.id for enrolment in user.enrolments
    ]:
        abort(404)
    else:
        return render_template('dashboard.html', user=user, cohort=cohort)


@user.route('/discussions/<int:id>')
@login_required
def discussions_get(id):
    eval = Eval.query.filter_by(id=id).one_or_none()

    if eval is None:
        abort(404)

    return render_template('discussion.html', eval=eval)


@user.route('/discussions/<int:id>', methods=['POST'])
@login_required
def discussions_post(id):
    eval = Eval.query.filter_by(id=id).one_or_none()

    if eval is None:
        abort(404)

    if eval.review is None:
        eval.review = request.form
    else:
        eval.feedback = request.form

    db_session.merge(eval)
    db_session.commit()

    return render_template('discussion.html', eval=eval)


@user.route('/resources/<int:cohort_id>')
@login_required
def resources(cohort_id):
    cohort = Cohort.query.filter_by(id=cohort_id).one_or_none()

    if cohort is None:
        abort(404)
    elif cohort.id not in [
        enrolment.cohort.id for enrolment in current_user.enrolments
    ]:
        abort(403)
    else:
        return render_template('resources.html', cohort=cohort)
