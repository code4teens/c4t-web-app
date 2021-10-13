from flask import Flask

from config import prod_config

app = Flask(__name__)
app.config.from_object(prod_config)


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
