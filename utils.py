import os

import pytz


class prod_config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')


tz = pytz.timezone('Asia/Kuala_Lumpur')

DPY_COC = os.environ.get('DPY_COC')
DPY_GUIDE = os.environ.get('DPY_GUIDE')

references = [DPY_COC, DPY_GUIDE]

DPY_D1 = os.environ.get('DPY_D1')
DPY_D2 = os.environ.get('DPY_D2')
DPY_D3 = os.environ.get('DPY_D3')
DPY_D4 = os.environ.get('DPY_D4')
DPY_D5 = os.environ.get('DPY_D5')
DPY_D6 = os.environ.get('DPY_D6')
DPY_D7 = os.environ.get('DPY_D7')
DPY_D8 = os.environ.get('DPY_D8')
DPY_D9 = os.environ.get('DPY_D9')

C4W_DPY_D1 = os.environ.get('C4W_DPY_D1')
C4W_DPY_D2 = os.environ.get('C4W_DPY_D2')
C4W_DPY_D3 = os.environ.get('C4W_DPY_D3')
C4W_DPY_D4 = os.environ.get('C4W_DPY_D4')
C4W_DPY_D5 = os.environ.get('C4W_DPY_D5')
C4W_DPY_D6 = os.environ.get('C4W_DPY_D6')

projects = [
    DPY_D1, DPY_D2, DPY_D3, DPY_D4, DPY_D5, DPY_D6, DPY_D7, DPY_D8, DPY_D9
]
c4w_projects = [
    C4W_DPY_D1, C4W_DPY_D2, C4W_DPY_D3, C4W_DPY_D4, C4W_DPY_D5, C4W_DPY_D6
]
