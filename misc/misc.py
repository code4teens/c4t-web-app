import re

from flask import Blueprint, request

from database import db_session
from models import Email
from config import make_json_response

misc = Blueprint('misc', __name__, template_folder='templates/misc')


@misc.route('/subscribe', methods=['POST'])
def subscribe():
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = request.get_data().decode("utf-8")

    if re.fullmatch(regex, email):
        existing_email = Email.query.filter_by(email=email).one_or_none()

        if existing_email is None:
            mail = Email(email=email)
            db_session.add(mail)
            db_session.commit()

            title = 'OK'
            detail = f'Success'

            return make_json_response(title, 200, detail)
        else:
            title = 'Conflict'
            detail = f'Email already exists'

            return make_json_response(title, 409, detail)
    else:
        title = 'Bad Request'
        detail = f'Invalid email'

        return make_json_response(title, 400, detail)
