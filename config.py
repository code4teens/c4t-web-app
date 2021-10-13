import os


class prod_config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
