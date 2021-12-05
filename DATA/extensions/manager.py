# ----------------------------------- #
# name: Extension Manager platform 1  #
# codename: XtMgr                     #
# author: Whmsft                      #
# contributors: None                  #
# ----------------------------------- #

import os
import sys
from pathlib import Path

PATH = str(Path(Path(__file__).parent.resolve()))


'''
BASIC TUTOR for extensions:

extensions here can have new blocks of code to modify WhirlEdit execution

the structure is like this:

directory Extensions:
    manager.py (the main manager)
    EXTENSION_NAME (a directory):
        main.py (main script file of the extension)

how will main.py look like?
it will have a string (basically a block of code you want to execute)
the string will be connected by this line:
tasks.{the place where you want your code}.append(--the block of code--)


a simple example:
main.py:
```
tasks.after_imports.append("""
print('imports imported...')
""")
```

this is quite simple.. :)
'''


class tasks:
    after_imports = []
    before_extension_installation = []
    after_extension_installation = []
    main_vars_definition = []
    main_funcs_definition = []
    main_classes_definition = []
    before_root_definition = []
    after_root_definition = []
    sidebar_widgets = []
    before_mainloop = []
    before_configs_save = []
    onexit = []

print('Extension Manager platform 1')

def getTask(task):
    for i in task:
        return i

def close():
    sys.exit()

print('scanning extension(s)')
for i in os.listdir(PATH):
    ipath = 'data/extensions/'+i
    if os.path.isdir(os.path.abspath(ipath)) and i != '__pycache__':
        print('Found extension: {}'.format(i))
    if os.path.isdir(os.path.abspath(ipath)) and i != '__pycache__':
        exec(open(ipath+'/__init__.py').read()) 
        print('loaded "{}"'.format(i))
