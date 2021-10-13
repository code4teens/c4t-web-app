from flask import abort, Flask, render_template
from flask_login import LoginManager

from auth import auth
from config import prod_config
from database import db_session
from models import User

app = Flask(__name__)
app.config.from_object(prod_config)
app.register_blueprint(auth)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    abort(401)


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).one_or_none()


@app.route('/')
def index():
    return render_template('index.html')


@app.teardown_appcontext
def close_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
