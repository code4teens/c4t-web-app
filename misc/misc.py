import re

from flask import Blueprint, request

from database import db_session
from models import Subscription

misc = Blueprint('misc', __name__, template_folder='templates/misc')


@misc.route('/subscribe', methods=['POST'])
def subscribe():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = request.get_data().decode("utf-8")

    if re.fullmatch(regex, email):
        existing_email = \
            Subscription.query.filter_by(email=email).one_or_none()

        if existing_email is None:
            mail = Subscription(email=email)
            db_session.add(mail)
            db_session.commit()
            data = {
                'title': 'OK',
                'status': 200,
                'detail': 'Success'
            }

            return data, 200
        else:
            data = {
                'title': 'Conflict',
                'status': 409,
                'detail': 'Email already exists'
            }

            return data, 409
    else:
        data = {
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Invalid email'
        }

        return data, 400
