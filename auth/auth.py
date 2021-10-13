import os

from flask import Blueprint, flash, render_template, request
import requests

auth = Blueprint('auth', __name__, template_folder='templates/auth')


@auth.route('/login')
def login_get():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    id = request.form.get('id')
    password = request.form.get('password')

    api = os.environ.get('API_URL')
    url = f'{api}/users/{id}/login'
    r = requests.post(url, json={'password': password})

    if r.status_code == 200:
        pass
    elif r.status_code == 401:
        flash('Invalid password.')
    elif r.status_code == 404:
        flash('Invalid username.')
    else:
        flash('An error occurred.')

    return render_template('login.html')
