import os

import pytz

tz = pytz.timezone('Asia/Kuala_Lumpur')


class prod_config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
