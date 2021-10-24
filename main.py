from flask import abort, Flask, render_template
from flask_login import LoginManager

from auth import auth
from config import prod_config
from database import db_session
from models import User
from user import user

app = Flask(__name__)
app.config.from_object(prod_config)
app.register_blueprint(auth)
app.register_blueprint(user)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).one_or_none()


@app.route('/')
def index():
    return render_template('index.html')


@app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()


@app.errorhandler(401)
def unauthorised_401(e):
    data = {
        "status": 401,
        "title": "Unauthorised",
        "detail": "You must be logged in to view this resource."
    }
    return render_template('error.html', **data)


@app.errorhandler(403)
def forbidden_403(e):
    data = {
        "status": 403,
        "title": "Forbidden",
        "detail": "Insufficient permission to access resource."
    }
    return render_template('error.html', **data)


@app.errorhandler(404)
def not_found_404(e):
    data = {
        "status": 404,
        "title": "Not Found",
        "detail": "The requested resource could not be found."
    }
    return render_template('error.html', **data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
