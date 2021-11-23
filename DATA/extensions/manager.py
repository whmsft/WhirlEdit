# ----------------------------------- #
# name: Extension Manager platform 1  #
# codename: XtMgr                     #
# author: Whmsft                      #
# contributors: None                  #
# ----------------------------------- #

import os
from pathlib import Path

PATH = str(Path(Path(__file__).parent.resolve()))

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
print('...')

for i in os.listdir(PATH):
    if os.path.isdir(i):
        exec(open(PATH+'/{}/main.py'.format(i)))
