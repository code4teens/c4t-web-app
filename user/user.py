from datetime import datetime, timedelta
from functools import wraps

from flask import abort, Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from database import db_session
from models import Cohort, Eval, User
from utils import c4t_projects, c4w_projects, dpy_references, tz

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
    return redirect(url_for('user.admin_cohorts'))


@user.route('/admin/cohorts')
@user.route('/admin/cohorts/<int:id>')
@admin_only
def admin_cohorts(id=None):
    if id is None:
        cohorts = Cohort.query.all()

        return render_template('admin_cohorts.html', cohorts=cohorts)
    else:
        cohort = Cohort.query.filter_by(id=id).one_or_none()

        if cohort is None:
            abort(404)

        return render_template('admin_cohort.html', cohort=cohort)


@user.route('/profile')
@login_required
def profile_redirect():
    return redirect(url_for('user.profile', id=current_user.id))


@user.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.filter_by(id=id).one_or_none()

    if user is None:
        abort(404)

    return render_template('profile.html', user=user)


@user.route('/dashboard')
@login_required
def dashboard_redirect():
    cohort_id = current_user.enrolments[-1].cohort.id

    return redirect(
        url_for(
            'user.dashboard', user_id=current_user.id, cohort_id=cohort_id
        )
    )


@user.route('/dashboard/<int:user_id>')
@user.route('/dashboard/<int:user_id>/<int:cohort_id>')
@admin_or_owner_only
def dashboard(user_id, cohort_id=None):
    user = User.query.filter_by(id=user_id).one_or_none()

    if user is None:
        abort(404)

    if cohort_id is None:
        cohort_id = user.enrolments[-1].cohort.id

        return redirect(
            url_for('user.dashboard', user_id=user.id, cohort_id=cohort_id)
        )
    else:
        cohort = Cohort.query.filter_by(id=cohort_id).one_or_none()

        if cohort is None:
            abort(404)

        if cohort.id not in [
            enrolment.cohort.id for enrolment in user.enrolments
        ]:
            abort(403)
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


@user.route('/resources')
@user.route('/resources/<int:cohort_id>')
@login_required
def resources(cohort_id=None):
    if cohort_id is None:
        cohort_id = current_user.enrolments[-1].cohort.id

        return redirect(url_for('user.resources', cohort_id=cohort_id))
    else:
        cohort = Cohort.query.filter_by(id=cohort_id).one_or_none()

        if cohort is None:
            abort(404)

        if cohort.id not in [
            enrolment.cohort.id for enrolment in current_user.enrolments
        ]:
            abort(403)
        else:
            c4t_dpy = [1, 2, 3, 4, 6]
            c4w_dpy = [5]

            if cohort.id in c4t_dpy:
                return render_template(
                    'resources_dpy.html',
                    cohort=cohort,
                    references=dpy_references,
                    projects=c4t_projects
                )
            elif cohort.id in c4w_dpy:
                return render_template(
                    'resources_c4w_dpy.html',
                    cohort=cohort,
                    references=dpy_references,
                    projects=c4w_projects
                )
            else:
                return render_template('resources.html', cohort=cohort)
