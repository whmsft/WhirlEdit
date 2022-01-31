import os
import shutil
shutil.rmtree('./Data/Lexers/__pycache__')
for i in os.listdir('./DATA/Lexers/'):
    if i != '__init__.py' or i != '__pycache__':
        exec('from . import {}'.format(i[:-3]))