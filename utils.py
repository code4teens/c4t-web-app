import os

import pytz


class prod_config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')


tz = pytz.timezone('Asia/Kuala_Lumpur')

DPY_COC = os.environ.get('DPY_COC')
DPY_GUIDE = os.environ.get('DPY_GUIDE')

dpy_references = [DPY_COC, DPY_GUIDE]

C4T_DPY_D1 = os.environ.get('C4T_DPY_D1')
C4T_DPY_D2 = os.environ.get('C4T_DPY_D2')
C4T_DPY_D3 = os.environ.get('C4T_DPY_D3')
C4T_DPY_D4 = os.environ.get('C4T_DPY_D4')
C4T_DPY_D5 = os.environ.get('C4T_DPY_D5')
C4T_DPY_D6 = os.environ.get('C4T_DPY_D6')
C4T_DPY_D7 = os.environ.get('C4T_DPY_D7')
C4T_DPY_D8 = os.environ.get('C4T_DPY_D8')
C4T_DPY_D9 = os.environ.get('C4T_DPY_D9')

C4W_DPY_D1 = os.environ.get('C4W_DPY_D1')
C4W_DPY_D2 = os.environ.get('C4W_DPY_D2')
C4W_DPY_D3 = os.environ.get('C4W_DPY_D3')
C4W_DPY_D4 = os.environ.get('C4W_DPY_D4')
C4W_DPY_D5 = os.environ.get('C4W_DPY_D5')

c4t_projects = [
    C4T_DPY_D1, C4T_DPY_D2, C4T_DPY_D3, C4T_DPY_D4, C4T_DPY_D5, C4T_DPY_D6,
    C4T_DPY_D7, C4T_DPY_D8, C4T_DPY_D9
]
c4w_projects = [C4W_DPY_D1, C4W_DPY_D2, C4W_DPY_D3, C4W_DPY_D4, C4W_DPY_D5]
