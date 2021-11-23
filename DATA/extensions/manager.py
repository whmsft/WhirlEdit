# ----------------------------------- #
# name: Extension Manager platform 1  #
# codename: XtMgr                     #
# author: Whmsft                      #
# contributors: None                  #
# ----------------------------------- #

import os
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
tasks.after_imports.append(--the block of code--)


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
    class after_imports:
        pass
    class before_extension_installation:
        pass
    class after_extension_installation:
        pass
    class main_vars_definition:
        pass
    class main_funcs_definition:
        pass
    class main_classes_definition:
        pass
    class before_root_definition:
        pass
    class after_root_definition:
        pass
    class sidebar_widgets:
        pass
    class before_scheme_definition:
        pass
    class before_mainloop:
        pass
    class before_configs_save:
        pass
    class onexit:
        pass

print('Extension Manager platform 1')

for i in os.listdir(PATH):
    if os.path.isdir(i):
        exec(open(PATH+'/{}/main.py'.format(i)))
        print('loaded "{}"'.format(i))
