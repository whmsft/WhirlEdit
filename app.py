
import re
import os
import sys
import zlib
import time
import yaml
import shutil
import urllib
import zipfile
import getpass
import zipfile
import textwrap
import datetime
import tempfile
import requests
import platform
import threading
import subprocess
import webbrowser
import ttkbootstrap
import tkinter as tk
import tkinter.font as tkfont
from confscript import dump
from confscript import read as cfsread
from wday import read
from tkinter import ttk
from pathlib import Path
from tkcode import CodeEditor
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from tkinter import *
from tkterminal import *
replaceitms = {
    "import DATA.extensions.manager as xtmgr": "import src.DATA.extensions.manager as xtmgr",
    "import data": "import src.data as data",
    "import widgets": "import src.widgets as widgets",
    "PATH = str(Path(Path(__file__).parent.resolve()))": "PATH = str(Path(Path(__file__).parent.resolve())) + '/src/'",
}
PATH = str(Path(Path(__file__).parent.resolve()))
import animation
import requests
indefined = ['Downloading (|)','Downloading (\)','Downloading (-)','Downloading (/)']

@animation.wait(indefined,speed=0)
def getfile(file):
    try:
        global pgr, num
        pgr = ['|','/','-','\\']
        url = file
        local_filename = PATH+'/upgrade.tmp'
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1):
                    f.write(chunk)
        zipfile.ZipFile(local_filename,'r').extractall(PATH)
        os.rename(PATH+'/WhirlEdit-main',PATH+'/src/')
        os.remove(local_filename)
        print('Done!')
    except:
        print('Failed..')
        print('some errors occured')

if len(sys.argv) > 1:
    if sys.argv[1] in ['up','update','upgrade','to-dev','--up','--update','--upgrade']:
        getfile('https://github.com/whmsft/WhirlEdit/archive/refs/heads/main.zip')

if os.path.isdir(PATH+'/src/'):
    print('looking for main file')
    sourcefile = open(PATH+'/src/main.py').read()
    for z in replaceitms.keys():
        sourcefile = sourcefile.replace(z,replaceitms[z])
    print('executing main sources')
    exec(sourcefile)
else:
    print('Source directory not found, Downloading it..')
    getfile('https://github.com/whmsft/WhirlEdit/archive/refs/heads/main.zip')
