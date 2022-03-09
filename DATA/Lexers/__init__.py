import os
import shutil
try:
    shutil.rmtree('./Data/Lexers/__pycache__')
except:
    pass
for i in os.listdir('./DATA/Lexers/'):
    if i not in '__init__.py__pycache__':
        exec('from . import {}'.format(i[:-3]))