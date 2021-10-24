from flask import abort, Blueprint, render_template, request
from flask_login import current_user, login_required

from database import db_session
from models import Cohort, Eval, User

user = Blueprint('user', __name__, template_folder='templates/user')


@user.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.filter_by(id=id).one_or_none()
    if user is None:
        abort(404)

    return render_template('profile.html', user=user)


@user.route('/dashboard/<int:id>')
@login_required
def dashboard(id):
    cohort = Cohort.query.filter_by(id=id).one_or_none()

    if cohort is None or cohort.id not in [
        enrolment.cohort.id for enrolment in current_user.enrolments
    ]:
        abort(404)
    else:
        return render_template('dashboard.html', cohort=cohort)


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
