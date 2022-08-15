# ----------------------------------------- #
# name: WhirlEdit                           #
# version: 5.dev                            #
# codename: thruster                        #
# author: whmsft                            #
# license: GNU GPLv3                        #
# platforms: Windows, Linux (maybe mac too) #
# ----------------------------------------- #

__version__ = 'v5.0.1 Thruster'

def execute(key):
    for i in key:
        exec(i)

from DATA import Lexers
import DATA.extensions.manager as xtmgr

import re
from pygments.lexer import *
from pygments.token import *

import os
import sys
import zlib
import data
import time
import yaml
import shutil
import urllib
import widgets
import zipfile
import getpass
import zipfile
import textwrap
import datetime
import tempfile
import requests
import platform
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

execute(xtmgr.tasks.after_imports)
start = time.time()
system = platform.platform().split('-')[0].lower()
PATH = str(Path(Path(__file__).parent.resolve()))
temp_dir = str(tempfile.gettempdir())

if not os.path.isdir(temp_dir+'/WhirlEdit/'):
	if not system=='windows':
		temp_dir = str(Path(Path(__file__).parent.resolve(), 'temp'))
		try:
			os.mkdir(temp_dir+'\\Whirledit\\')
		except: pass

def getfile(file):
    pgr = ['|','/','-','\\']
    url = file
    try:
        leng = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print("Package not found in repositories\nyou can check yourself at {}\nIf this is a mistake, then please report".format("https://whmsft.github.io/extensions/"))
        exit()
    local_filename = temp_dir+"/whirledit/"+file.split("/")[-1]
    num = 0
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if num == 4:
                    num = 0
                else:
                    num += 1
                f.write(chunk)
                print('installing {} [{}]'.format(local_filename.replace('.pkg.zip',''),pgr[num]))
    zipfile.ZipFile(local_filename,'r').extractall(PATH)
    print("installed {} {}".format(sys.argv[1],local_filename.replace(".pkg.zip","")))

execute(xtmgr.tasks.before_extension_installation)

if len(sys.argv) > 1:
    if sys.argv[1] in ["package","pkg","plugin"]:
        for i in sys.argv[2:]:
            pkgname = i
            getfile("https://whmsft.github.io/extensions/"+pkgname+'.pkg.zip')
        exit()

execute(xtmgr.tasks.after_extension_installation)

print("Whirledit {} running on {} {}".format(__version__,system,'deXtop' if system == 'linux' else 'desktop'))

def updateforever():
    update()
    mainwindow.after(10,updateforever)

def auto_indent(event):
    global line
    text = event.widget
    line = text.get("insert linestart", "insert")
    match = re.match(r'^(\s+)', line)
    whitespace = match.group(0) if match else ""
    text.insert("insert", f"\n{whitespace}")
    return "break"

def log_call(message, call="INTERNAL"):
    logs = '{} [{}]: {}'.format(round(time.time()-start, 2), call, message)
    print(logs)

def Tab_reorder(event):
    try:
        index = notebook.index(f"@{event.x},{event.y}")
        notebook.insert(index, child=notebook.select())
    except tk.TclError:
        pass

def smartdeletetab(event):
    try:
        index = notebook.index(f"@{event.x},{event.y}")
        notebook.forget(index)
    except tk.TclError:
        pass

def log_fake(message, call='INTERNAL'):
    logs = '{} [{}]: {}'.format(round(time.time()-start,2),call,message)

def greet_time():
    hour =  int(str(datetime.datetime.now().time()).split(':')[0])
    return (
        "morning"
        if 5 <= hour <= 11
        else "afternoon"
        if 12 <= hour <= 17
        else "evening"
        if 18 <= hour <= 22
        else "night"
    )

# runners' file
try:
    configs = open(PATH+"/DATA/runner.confscript", "r+")
except FileNotFoundError:
    configs = open(PATH+"/DATA/runner.confscript", "x")

datafile = open(PATH+"/DATA/runner.confscript").read()
if datafile.isspace():
    isConf = False
else:
    isConf = True

# define <logs> function
if data.configuration['Features']['Logging']:
    log = log_call
else:
    log = log_fake

# define <main> variable(s)
frames = {}
filepath = ""
colors = []
extension = {}
openedfolders = []
nothing = [1,0,1,1,1,1]
tabfmt = {}
note        = {}
openedfiles = {}
canvas      = {}
scrolly     = {}
scrollx     = {}
var         = 0

highlight = {}
'''
    "Ada"         : [".adb",".ads"],
    "Bash"        : [".sh",".csh",".ksh"],
    "Batch"       : [".cmd",".bat"],
    "BrainFuck"   : [".b",".bf"],
    "C"           : [".c",".h"],
    "CMake"       : [],
    "CoffeeScript": [".coffee",".cson",".litcoffee"],
    "CSS"         : [".css"],
    "C#"          : [".cs",".csx"],
    "C++"         : [".cc",".cpp",".cxx",".c++",".hh",".hpp",".hxx",".h++"],
    "Dart"        : [".dart"],
    "Delphi"      : [".dpr"],
    "Dockerfile"  : [".dockerfile"],
    "Fortran"     : [".f",".f90",".f95"],
    "Go"          : [".go"],
    "Groovy"      : [".groovy",".gvy",".gradle",".jenkinsfile"],
    "Haskell"     : [".hs",".lhs"],
    "HTML"        : [".htm",".html",".xml",'.svg'],
    "Java"        : [".java",".jar",".class"],
    "JavaScript"  : [".js",".cjs",".mjs"],
    "JSON"        : [".json"],
    "Kotlin"      : [".kt",".kts",".ktm"],
    "Lisp"        : [".lsp"],
    "Lua"         : [".lua"],
    "MATLAB"      : [".m",".p",".mex",".mat",".fig",".mlx",".mlapp",".mltbx"],
    "MakeFile"    : [".make",".makefile"],
    "NASM"        : [".asm",".asm",".inc"],
    "Objective-C" : [".mm"],
    "Perl"        : [".plx",".pl",".pm",".xs",".t",".pod"],
    "PHP"         : [".php",".phar",".phtml",".pht",".phps"],
    "Powershell"  : [".ps1"],
    "Python"      : [".py",".pyi",".pyc",".pyd",".pyo",".pyw",".pyz"],
    "R"           : [".r",".rdata",".rds",".rda"],
    "Ruby"        : [".rb"],
    "Swift"       : [".swift"],
    "SQL"         : [".sql"],
    "Tcl"         : [".tcl",".tbc"],
    "TypeScript"  : [".ts",".tsx"],
    "Vim"         : [".vim"],
    "YAML"        : [".yaml",".yml"],
}'''

list_of_lexers = os.listdir(PATH+'/DATA/Lexers/')
list_of_lexers.remove('__pycache__')
list_of_lexers.remove('__init__.py')
for i in range(len(list_of_lexers)):
    list_of_lexers[i] = list_of_lexers[i].replace('.py', '')
for i in list_of_lexers:
    temp_filenames = eval("Lexers.{}.{}.filenames".format(i,i))
    for x in range(len(temp_filenames)):
        temp_filenames[x] = temp_filenames[x][1:]
    print(temp_filenames)
    highlight[i] = temp_filenames
print(highlight)

execute((xtmgr.tasks.main_vars_definition))

def about(*args):
    log('opening about')
    def nothingmod(_pos, val, ext=None):
        nothing[_pos] = val
        a.destroy()
    if nothing[4] == 1:
        windowWidth = 300
        windowHeight = 320
        xCordinate = int((screenWidth/2) - (windowWidth/2))
        yCordinate = int((screenHeight/2) - (windowHeight/2))
        a = tk.Toplevel(mainwindow)
        nothing[4] = 0
        if system == 'windows':
            a.wm_attributes('-topmost', 'true', '-toolwindow', 'true')
        else:
            a.wm_attributes('-topmost', 'true')
        a.title('Whirledit')
        a.resizable(False, False)
        try:
            a.iconbitmap(PATH+"/DATA/icons/favicon.ico")
        except: # errors on replit's Ubuntu system
            pass
        a.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))
        z = Label(a, image=logoIMG)
        z.pack(pady=5, padx=5)
        b = Label(a, text='WhirlEdit', font='Consolas 20')
        b.pack()
        c = Label(a, text=__version__, font='Consolas 10')
        c.pack()
        d = Label(a, text='\nWritten in Python\nby whmsft\n',font='Consolas 15')
        d.pack()
        e = ttk.Button(a, text='GitHub',
                       command=lambda: webbrowser.open('http://github.com/whmsft/WhirlEdit'))
        e.pack(padx=10,pady=10)
        a.protocol("WM_DELETE_WINDOW", lambda: nothingmod(4, 1))
    else:
        pass


def fullscreen(*args):
    if nothing[1] == 0:
        log('on', call='FULLSCREEN')
        mainwindow.wm_attributes("-fullscreen",1)
        nothing[1] = 1
    else:
        log('off', call='FULLSCREEN')
        mainwindow.wm_attributes("-fullscreen",0)
        nothing[1] = 0


def set_syntax(lang):
    note[current_note()].config(language=lang)
    log(lang, call='SYNTAX')

def togglesetti(*args):
    global nothing
    if nothing[5] == 0:
        splitter.forget(settipaneframe)
        nothing[5] = 1
    else:
        splitter.add(settipaneframe,before=root,width=220)
        splitter.forget(runnerpaneframe)
        splitter.forget(filespaneframe)
        splitter.forget(lookspaneframe)
        nothing[5] = 0


def togglesidepane(*args):
    global nothing
    if nothing[0] == 0:
        splitter.forget(filespaneframe)
        nothing[0] = 1
    else:
        splitter.add(filespaneframe, before = root,width=220)
        splitter.forget(lookspaneframe)
        splitter.forget(runnerpaneframe)
        splitter.forget(settipaneframe)
        nothing[0] = 0


def togglelookpane(*args):
    global nothing
    if nothing[2] == 0:
        splitter.forget(lookspaneframe)
        nothing[2] = 1
    else:
        splitter.add(lookspaneframe, before = root,width=220)
        splitter.forget(filespaneframe)
        splitter.forget(runnerpaneframe)
        splitter.forget(settipaneframe)
        nothing[2] =0


def togglerunner(*args):
    global nothing
    if nothing[3] == 0:
        splitter.forget(runnerpaneframe)
        nothing[3] = 1
    else:
        splitter.add(runnerpaneframe, before = root,width=220)
        splitter.forget(filespaneframe)
        splitter.forget(lookspaneframe)
        splitter.forget(settipaneframe)
        nothing[3] =0

def update(*args):
    thisfile = ""
    greet['text']= 'Good {}, {}'.format(greet_time(), getpass.getuser())
    try:
        if openedfiles[current_note()] == '' or openedfiles[current_note()] == ' ':
            thisfile = 'None'
        else:
            thisfile = openedfiles[current_note()]
        root.update()
        cursyntax.set(identify(tabfmt[current_note()]))
        fdir = "/".join(openedfiles[current_note()].split("/")[:-1])
        my_line = note[current_note()].index(tk.INSERT).split('.')
        note[current_note()]['font'] = data.config['Looks']['Font']['Font']+" "+data.config['Looks']['Font']['Size']
        note[current_note()]['blockcursor'] = data.isBlockcursor
        status['text'] = "File: {} | Line {}, Column {}".format(thisfile, my_line[0], my_line[1])
        if fdir in openedfolders or fdir in PATH+'/':
            pass
        else:
            framed.add(fdir)
            openedfolders.append(fdir)
            log('added {}'.format(fdir), call='FOLDER')
    except:
        pass

def openthisfile(event):
    global extension
    global filepath
    if notebook.select() == "":
        newTab()
    item_id = event.widget.focus()
    item = event.widget.item(item_id)
    values = item['text']
    print(item)
    if os.path.isfile(values):
        try:
            variable = current_note()
            filepath = values
            print(filepath.lower())
            if filepath.lower().endswith('.ppm') or filepath.lower().endswith('.png') or filepath.lower().endswith('.jpg') or filepath.lower().endswith('.gif'):
                local_image = tk.PhotoImage(file=filepath)
                note[current_note()].window_create(tk.END, window=tk.Label(note[current_note()], image=local_image))
            else:
                extension[current_note()] = "."+filepath.split(".")[-1]
                note[variable].delete(1.0, END)
                file = open(filepath, "r")
                note[current_note()]["language"] = identify(filepath.split("/")[-1])
                note[variable].insert(1.0, file.read())
                openedfiles[variable] = filepath
                file.close()
                log('opened {}'.format(filepath, call='FILE'))
                notebook.tab(frames[variable], text=filepath.split("/")[-1]+"   ")
                note[current_note()].config(language=identify("."+filepath.split(".")[-1]))
        except UnicodeDecodeError as uce:
            log('({}) {}'.format(type(uce).__name__, uce), call='FILES')
            showerror(type(uce).__name__, uce)


def changekeybind(*args):
    def getit__(index):
        data.config['Key Bindings'][theselabels[i]['text']] = theseentries[i].get()
    menu = tk.Toplevel(mainwindow)
    theseframes  = {}
    theselabels  = {}
    theseentries = {}
    listss = []
    for i in data.config['Key Bindings'].keys():
        listss.append(i)
    for i in range(len(data.config['Key Bindings'].keys())):
        theseframes[i] = ttk.Frame(menu)
        theselabels[i] = tk.Label(theseframes[i], text=listss[i])
        theselabels[i].pack(side='left', fill='x')
        theseentries[i] = ttk.Entry(theseframes[i])
        theseentries[i].insert(0, data.config['Key Bindings'][listss[i]])
        theseentries[i].pack(side='right', fill='x')
        theseentries[i].bind('<Return>', lambda i=i: getit__(i))
        theseframes[i].pack(fill='x', side='bottom')
    tk.Label(menu, text='Info: Change the entries and hit <Return> to save').pack()
    menu.mainloop()

execute((xtmgr.tasks.main_funcs_definition))

class Settings(object):
    def savechangesSETTINGS(self):
        data.config['Looks']['Theme']['Folder']  = self.themeFolder.get()
        data.config['Looks']['Theme']['Default'] = self.themeName.get()
        data.config['Looks']['Scheme']['Folder'] = PATH+self.schemeFolder.get()
        log('modified',call='SETTINGS')
    def __init__(self,master):
        frame = tk.Frame(master)
        setlooks = ttk.LabelFrame(frame,text='Looks')
        settheme = ttk.LabelFrame(setlooks,text='Theme')
        setscheme = ttk.LabelFrame(setlooks,text='Scheme')

        label01 = tk.Label(settheme,text='Folder:').pack()
        self.themeFolder = ttk.Entry(settheme, font='Consolas',width=15)
        self.themeFolder.pack(fill='x')
        self.themeFolder.insert(0, data.config['Looks']['Theme']['Folder'])
        label02 = ttk.Label(settheme,text='Use theme:').pack()
        self.themeName =ttk.Entry(settheme,font='Consolas')
        self.themeName.pack(fill='x')
        self.themeName.insert(0, data.config['Looks']['Theme']['Default'])
        label03 = ttk.Label(setscheme,text='Folder').pack()
        self.schemeFolder= ttk.Entry(setscheme,font='Consolas')
        self.schemeFolder.pack(fill='x')
        self.schemeFolder.insert(0, data.config['Looks']['Scheme']['Folder'])

        labelrubbish1 = tk.Label(frame,text=' ')

        keybindchangebtnfor_settings = ttk.Button(frame,text='Change Key Bindings',command = lambda:changekeybind())

        settheme.pack(side='top', fill='both')
        setscheme.pack(side='top', fill='both')
        setlooks.pack(side='top', fill='both')

        labelrubbish1.pack()
        keybindchangebtnfor_settings.pack(fill='x')
        savebtn = ttk.Button(frame, text='Confirm & save', command=self.savechangesSETTINGS)
        savebtn.pack(pady=15,padx=5,fill='x')
        frame.pack(expand=True, fill='both')


class RunnerPane(object):
    def __init__(self,master):
        frame = tk.Frame(master)
        if system == "windows":
            self.button = ttk.Button(frame,text='Open CMD', command=lambda: opencmd())
            widgets.create_tool_tip(self.button, text='open Windows Command Processor (cmd)\nin the current directory')
        self.rubbish0 = tk.Label(frame,text=' ')
        self.rubbish0.grid()
        self.l1 = tk.Label(frame,text='  ')
        self.l1.grid(row=2,column=0)
        self.runners = ['This runner']
        self.rns = tk.Menu(frame)
        for i in get_confs():
            if i != "@":
                self.rns.add("command",label = i, command = lambda i=i: runner_conf(i))
        self.chooserunner = ttk.Menubutton(frame, menu=self.rns,text = 'Run current file with')
        widgets.create_tool_tip(self.chooserunner, text="Choose the runner to run\nthe currently opened\ntab..")
        self.chooserunner.grid(row=2,column=1, sticky='nsew')
        self.rubbish1 = tk.Label(frame,text=' ')
        self.rubbish1.grid()
        if system == "windows": self.button.grid(row=4, column=1)
        self.rubbish2=tk.Label(frame,text=' ').grid()
        self.newrunbtn = ttk.Button(frame, text = 'New Runner', command=lambda:new_runner())
        self.newrunbtn.grid(row=6, column=1)
        widgets.create_tool_tip(self.newrunbtn, text='Create a new runner \nand save to\nrunners file')
        frame.grid()


class LooksPane(object):
    def configsave(self,*args):
        if self.g.get() =='':
            pass
        else:
            mainwindow.title(self.g.get())
            data.config['Looks']['WindowTitle'] = mainwindow.title()
        data.font = self.i.get()
        data.config['Looks']['Font']['Font'] = r"\ ".join(data.font.split()[0:-1])
        data.config['Looks']['Font']['Size'] = data.font.split()[-1]
        data.isBlockcursor = self.isBlockcursor.get()
        data.config['Looks']['Font']['BlockCursor'] = self.isBlockcursor.get()
        data.config['Looks']['Scheme']['Default'] = self.curscheme.get()
        log('Changed',call='CONFIG')

    def __init__(self,master):
        frame = tk.Frame(master)
        self.curscheme = tk.StringVar()
        self.curscheme.set(data.config['Looks']['Scheme']['Default'])
        curscheme_values = [data.config['Looks']['Scheme']['Default']]
        for i in os.listdir(PATH+data.configuration['Looks']['Scheme']['Folder']):
            if i.lower().endswith('.json'):
                curscheme_values.append(i[:-5])
        self.b = ttk.OptionMenu(frame, self.curscheme, *curscheme_values, command = lambda a='s':note[current_note()].config(highlighter = PATH+data.configuration['Looks']['Scheme']['Folder']+self.curscheme.get()+'.json'))
        self.d = tk.Label(frame,text='Syntax')
        widgets.create_tool_tip(self.b, text='Select The color-scheme\nto use..')
        self.d.grid(row=2, column=0)
        self.e = tk.Label(frame,text='Scheme')
        self.e.grid(row=3, column=0)
        cursyntax = StringVar()
        languages = ['Choose']
        for i in highlight.keys():
            languages.append(i)
        self.c = ttk.OptionMenu(frame, cursyntax, *languages,command=lambda name="__main__": note[current_note()].config(language=cursyntax.get()))
        self.c.grid(row=2,column=1, pady=5)
        widgets.create_tool_tip(self.c, text='Select the programming language\nsyntax to use')
        self.b.grid(row=3,column=1,pady=5)
        self.f = tk.Label(frame,text='Window Title')
        self.f.grid(row=4,column=0,pady=5)
        self.g = ttk.Entry(frame,width=20)
        widgets.create_tool_tip(self.g, text='Add a new window title')
        self.g.grid(row=4,column=1,pady=5)
        self.h = tk.Label(frame,text='Font:')
        self.curfont=StringVar()
        self.curfont.set('{} {}'.format(data.configuration['Looks']['Font']['Font'], str(data.configuration['Looks']['Font']['Size'])))
        self.j = tk.Label(frame,text='Font')
        self.j.grid(row=5,column=0,pady=5)
        self.i = ttk.Entry(frame, text= self.curfont.get())
        widgets.create_tool_tip(self.i, text='Write the font to be used\nsyntax: "NAME SIZE"')
        self.i.insert(0,self.curfont.get())
        self.i.grid(row=5,column=1, pady=5)
        self.k = tk.Label(frame,text='Block Cursor')
        self.k.grid(row=6,column=0, pady=5)
        self.isBlockcursor = BooleanVar()
        self.isBlockcursor.set(data.config['Looks']['Font']['BlockCursor'])
        self.j = tk.Checkbutton(frame, variable=self.isBlockcursor, relief='flat', borderwidth=0)
        widgets.create_tool_tip(self.j, text='Shall you use Block Cursor\ninstead of normal "thin" one?')
        self.j.grid(row=6, column=1, sticky='w')
        rubbish1 = tk.Label(frame)
        rubbish1.grid()

        self.configconfirm = ttk.Button(frame,text="Save", command=self.configsave)
        self.configconfirm.grid(row=8,column=0)
        frame.grid(sticky='NEWS')


class PathView(object):
    def add_openfold(self):
        the_folder = askdirectory()
        self.add(the_folder)
        log('added '+the_folder, call='FOLDER')

    def add(self, path):
        abspath = os.path.abspath(path)
        self.insert_node('', abspath.split('\\')[-1], abspath)
        self.tree.bind('<<TreeviewOpen>>', self.open_node)

    def __init__(self, master, paths):
        main = tk.PanedWindow(master,handlesize=5,orient=VERTICAL)
        main.pack(expand=True, fill='both')
        tabspane = tk.Frame(main)
        listbox = tk.Listbox(tabspane)
        listbox.pack(expand=True, fill='both')
        #tabspane.pack(fill=BOTH,expand=1)
        frame = tk.Frame(main)
        nf = tk.Frame(frame)
        self.newfilebtn = ttk.Button(nf, image=projectBar_icon_newfile, style='secondary.TButton',command= lambda:newTab())
        self.newfilebtn.grid(row=0, column=0, pady=5, padx=5)
        self.newfoldbtn = ttk.Button(nf,image=projectBar_icon_newfold, style='secondary.TButton',command = lambda:self.add_openfold())
        self.newfoldbtn.grid(row=0, column=1, pady=5, padx=5)
        self.closetabtn = ttk.Button(nf, image=projectBar_icon_closefi, style='secondary.TButton',command=lambda:deltab())
        self.closetabtn.grid(row=0, column=2, pady=5, padx=5)
        widgets.create_tool_tip(self.newfilebtn, text='New Tab')
        widgets.create_tool_tip(self.newfoldbtn, text='Add Folder')
        widgets.create_tool_tip(self.closetabtn, text='Close Tab')
        nf.pack(side='top', fill='x')
        self.tree = ttk.Treeview(frame)
        self.tree.bind("<Double-Button-1>", openthisfile)
        self.nodes = dict()
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        #xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=ysb.set)#,xscrollcommand=xsb.set)
        self.tree.heading('#0', text='FOLDERS')
        self.tree.column('#0', width=50, minwidth=100)
        ysb.pack(side=RIGHT, fill=Y)
        #xsb.pack(side=BOTTOM,fill=X)
        self.tree.pack(fill=BOTH, expand=1)
        frame.pack(fill=BOTH, expand=1)
        for path in paths:
            abspath = os.path.abspath(path)
            self.insert_node('', abspath, abspath)
            self.tree.bind('<<TreeviewOpen>>', self.open_node)

    def insert_node(self, parent, text, abspath):
        node = self.tree.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            self.nodes[node] = abspath
            self.tree.insert(node, 'end')

    def open_node(self, event):
        node = self.tree.focus()
        abspath = self.nodes.pop(node, None)
        if abspath:
            self.tree.delete(self.tree.get_children(node))
            for p in os.listdir(abspath):
                self.insert_node(node, p, os.path.join(abspath, p))

execute((xtmgr.tasks.main_classes_definition))

def identify(extension):
    for y in highlight.keys():
        for z in highlight[y]:
            if extension == z:
                return y

def runner_conf(thisType):
    cmds = cfsread(datafile)
    command = cmds[thisType]['command']
    command = command.replace("$file", '"'+filepath+'"')
    base = filepath.split("/")[-1]
    base = base[:base.find(".")]
    command = command.replace("$base", base.replace(" ", "_"))
    command = command.replace("$dir", '"'+"/".join(filepath.split("/")[:-1])+'"')
    log('started {} via {}'.format(filepath, thisType), call='RUNNER')
    cmd = "start cmd /k {}".format(command)
    tkterminal.run_command(command)
    #subprocess.call(cmd, shell=True)


def get_confs():
    confs = []
    cmds = cfsread(datafile)
    for i in cmds.keys():
        confs.append(i)
    return confs

def new_runner():
    global configs
    configs = open(PATH+"/DATA/runner.confscript","r+")
    log('new runner dialog opened')
    global conf

    def done():
        global datafile
        global configs
        thisconf = ""
        datafile=datafile+'---\n{}'.format(dump({name.get():{'command':entry.get(),'extensions':entriee.get()}}))
        configs.write(datafile)
        configs.close()
        conf.quit()
        log('created {}'.format(name.get()), call='RUNNER')
    def helpwindow():
        a = tk.Toplevel(root)
        a.wm_attributes('-topmost', 'true', '-toolwindow', 'true')
        a.resizable(False,False)
        a.iconbitmap(PATH+"/DATA/icons/favicon.ico")
        a.title("Help")
        b = Label(a, text='Keywords', font="Consolas", anchor='w').pack(expand=True)
        b = Label(a, text='$file: filepath', font="Consolas", anchor='w').pack(expand=True)
        b = Label(a, text='$base: file base name', font="Consolas", anchor='w').pack(expand=True)
        b = Label(a, text='$dir: file directory', font="Consolas", anchor='w').pack(expand=True)
        b = Label(a, text='\nNOTE: only click "Confirm" & close\nnew runner popup to avoid errors', font="Consolas 12 \ bold", anchor='w').pack(expand=True)
        a.mainloop()
    conf = tk.Toplevel(root)
    conf.wm_attributes("-topmost", 1)
    conf.iconbitmap(PATH+"/DATA/icons/favicon.ico")
    conf.resizable(False, False)
    conf.title("Configure new Runner")
    conf.geometry("400x250")
    gui = BooleanVar()
    label = Label(conf, text="Runner Name", font="consolas")
    name = ttk.Entry(conf, width=25, font="consolas")
    name.place(x=150, y=10)
    label.place(x=10, y=16)
    label = Label(conf,text="Command", font="consolas")
    label.place(x=10, y=55)
    entry = widgets.AutocompleteEntry(conf, width=25, font="consolas")
    entry.set_completion_list((u'$file', u'$base', u'$dir', u'/k'))
    entry.place(x=150, y=50)
    entry.insert(0, 'compiler -o $base $file')
    label = Label(conf, text='Extensions',font='consolas')
    label.place(x=10, y=100)
    entriee = ttk.Entry(conf, width=25, font='Consolas')
    entriee.place(x=150, y=95)
    entriee.insert(0, '.py,.cpp,.h')
    helptxt = Label(conf, text="Do you need some", font="consolas")
    helptxt.place(x=60, y=150)
    helpbtn = ttk.Button(conf, text="Help", command=lambda: helpwindow())
    helpbtn.place(x=220, y=150)
    submit = ttk.Button(conf, text="Confirm", command=lambda: done())
    submit.place(x=125, y=200)
    conf.mainloop()


def runconf(*args):
    evaled = cfsread(datafile)
    for i in evaled.keys():
        for x in evaled[i]['extensions']:
            if extension[current_note()] in x:
                thisext = i
    try:
        runner_conf(thisext)
    except:
        pass
execute((xtmgr.tasks.before_root_definition))
theme_file = PATH+"{}/{}.json".format(data.configuration['Looks']['Theme']['Folder'],data.configuration['Looks']['Theme']['Default'])
mainwindow = ttkbootstrap.Style(theme = data.configuration['Looks']['Theme']['Default'],themes_file=theme_file).master
execute((xtmgr.tasks.after_root_definition))
log('Main Window created')
try:
    mainwindow.iconbitmap(PATH+"/DATA/icons/favicon.ico")
except tk.TclError:
    log('icon adding error')
else:
    log('icon added')
mainwindow.title(data.configuration['Looks']['WindowTitle'])
log('title set')
windowWidth = 800
windowHeight = 550
screenWidth  = mainwindow.winfo_screenwidth()
screenHeight = mainwindow.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
mainwindow.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))
log('geometry set')
style = ttk.Style(mainwindow)

statusbar = tk.Frame(mainwindow)
statusbar.pack(side='bottom', anchor='s', fill='x')

status = Label(statusbar, text = 'Welcome to WhirlEdit {}'.format(__version__), anchor='w')
status.pack(side='left')

cursyntax = StringVar()
languages = [data.config['Looks']['InitialSyntax']]
for i in highlight.keys():
    languages.append(i)

def givename_ext(lang):
    return highlight[lang][0]

def syntaxchange(*args):
    print(cursyntax.get())
    tabfmt[current_note()] = givename_ext(cursyntax.get()) # give extension on language name
    #note[current_note()].config(language=cursyntax.get())
    print(current_note())
    print(note)
    print('Lexers.{}.{}'.format(cursyntax.get(),cursyntax.get()))
    note[current_note()].lexer = eval('Lexers.{}.{}'.format(cursyntax.get(),cursyntax.get()))

syntaxchoose = ttk.OptionMenu(statusbar, cursyntax, *languages,command=syntaxchange, style='primary.Outline.TButton')
#syntaxchoose.config(indicatoron=False, bd=0, relief='flat')
syntaxchoose.pack(side='right')

rootframe = tk.PanedWindow(mainwindow, handlesize=5, orient=tk.VERTICAL)
rootframe.pack(side='right', expand=True, fill='both')
splitter = tk.PanedWindow(rootframe, handlesize=5, orient=tk.HORIZONTAL)

filespaneframe = tk.Frame(splitter)
lookspaneframe = tk.Frame(splitter)
settipaneframe = tk.Frame(splitter)

toolbar = ttk.Frame(mainwindow)
toolbar.pack(fill='both', expand=True)
toolbar_menu_icon = PhotoImage(file=data.icons.logo_mini, master=toolbar).subsample(5)
toolbar_menu = ttk.Button(toolbar, image=toolbar_menu_icon, command=about, style='primary.Link.TButton')
toolbar_menu.pack(fill='x')
tools_files_icon = PhotoImage(file=data.icons.sidebar_files,master=toolbar)
tools_files = ttk.Button(toolbar, image=tools_files_icon, command=togglesidepane, style='primary.Link.TButton')
tools_files.pack(fill='x')
tools_runner_icon = PhotoImage(file=data.icons.sidebar_runner,master=toolbar)
tools_runner = ttk.Button(toolbar, image=tools_runner_icon, command=togglerunner, style='primary.Link.TButton')
tools_runner.pack(fill='x')
tools_looks_icon = PhotoImage(file=data.icons.sidebar_looks,master=toolbar)
tools_looks = ttk.Button(toolbar, image=tools_looks_icon, command=togglelookpane, style='primary.Link.TButton')
tools_looks.pack(fill='x')
tools_settings_icon = PhotoImage(file=data.icons.sidebar_settings,master=toolbar)
tools_settings = ttk.Button(toolbar,image=tools_settings_icon, command=togglesetti, style='primary.Link.TButton')
tools_settings.pack(side='bottom', anchor='s', fill='x')

execute((xtmgr.tasks.sidebar_widgets))

log('Icons made and added', call='SIDEBAR')

projectBar_icon_newfile = PhotoImage(file=data.icons.project_newfile,master=toolbar)
projectBar_icon_newfold = PhotoImage(file=data.icons.project_newfolder,master=toolbar)
projectBar_icon_closefi = PhotoImage(file=data.icons.project_closefile,master=toolbar)

logoIMG = tk.PhotoImage(data=zlib.decompress(data.icons.logo))

root = tk.PanedWindow(splitter, orient=VERTICAL, handlesize=5)

runnerpaneframe = tk.Frame(splitter)
framed = PathView(filespaneframe, paths=[])
settingpane = Settings(settipaneframe)
lookpane = LooksPane(lookspaneframe)
runpane = RunnerPane(runnerpaneframe)

splitter.add(root)

if data.configuration['Features']['Terminal']:
    def termreset():
        global tkterminal
        tkterminal.pack_forget()
        tkterminal = Terminal(termframe, font='Consolas 10')
        tkterminal.basename = "$"
        tkterminal.shell = True
        tkterminal.pack(side='left', anchor='w', fill='both', expand=True)
        log('reset', call='TERMINAL')

    termframe = ttk.Frame()
    termicon_clear = PhotoImage(file= data.icons.terminal_clear)
    termicon_reset = PhotoImage(file= data.icons.terminal_reset)
    tkterminal = Terminal(termframe, font='Consolas 10', relief='flat')
    tkterminal.basename = "$"
    tkterminal.shell = True
    newframe = tk.Frame(termframe)
    newframe.pack(side='right',anchor='ne')
    tkterm_clear = ttk.Button(newframe,style='secondary.Link.TButton',image=termicon_clear,  command=lambda:tkterminal.clear())#anchor='n',relief='flat',borderwidth=0,
    tkterm_reset = ttk.Button(newframe,style='secondary.Link.TButton',image=termicon_reset, command=lambda:termreset())#anchor='n',relief='flat', borderwidth=0,
    widgets.create_tool_tip(tkterm_clear, "Clear the terminal")
    widgets.create_tool_tip(tkterm_reset, "Restart the terminal\nJust in case you crashed..")
    tkterm_clear.pack(side='top')
    tkterm_reset.pack(side='top')
    tkterminal.pack(side='left',anchor='w',fill='both',expand=True)
    log('placed',call='TERMINAL')
    termframe.pack(fill='both',expand=True)
    rootframe.add(splitter,height=400)
    root.add(termframe,height=180)
else:
    rootframe.add(splitter, height=400)

try:
    default_highlight = PATH+data.configuration['Looks']['Scheme']['Folder']+data.configuration['Looks']['Scheme']['Default']+'.json'
    log('set scheme {}'.format(default_highlight),call='LOOKS')
except Exception as e:
    log('({}) {}'.format(type(e).__name__, e), call='ERROR')
    showerror(type(e).__name__, e)
    sys.exit()

def opencmd(*args):
    try:
        if filepath == "":
            cwd = os.getcwd()
        else:
            cwd = "/".join(filepath.split("/")[:-1])
        drive = cwd[:2]
        log('cmd starting at {}'.format(cwd), call='RUNNER')
        subprocess.call('start cmd /k cd /d "{}"'.format(cwd), shell=True)
    except:
        subprocess.call('start cmd /k "{}"'.format(openedfiles[current_note()]), shell=True)

def runfile(*args):
    try:
        cwd = "/".join(filepath.split("/")[:-1])
        drive = cwd[:3]
        log('cmd starting for {}'.format(openedfiles[current_note()]), call='RUNNER')
        subprocess.call('start cmd /k "{}"'.format(openedfiles[current_note()]), shell=True)
    except:
        subprocess.call('start cmd /k "{}"'.format(openedfiles[current_note()]), shell=True)

def getpos(*args):
    global pos
    global line
    pos = note[int(current_note())].index("end")
    pos = pos[:-2]
    pos = int(pos)
    pos = pos -1
    line.set(pos)

def current_note():
    variable = notebook.select()
    if str(notebook.select()).replace('.!panedwindow.!panedwindow.!panedwindow.!notebook.!frame','') == "":
        variable = 1
    else:
        variable = int(str(notebook.select()).replace('.!panedwindow.!panedwindow.!panedwindow.!notebook.!frame',''))
        if variable == 0:
            pass
        else:
            variable = int(variable)
    return variable

def deltab(*args):
    try:
        if openedfiles[current_note()] == "":
            notebook.forget(notebook.select())
        else:
            if open(openedfiles[current_note()]).read() == note[current_note()].get(1.0,END):
                notebook.forget(notebook.select())
            else:
                optionchoosen = askyesnocancel("Save file?", "Save unsaved changes in {}".format(notebook.tab(notebook.select(), "text")))
                if optionchoosen == True:
                    saveFile()
                elif optionchoosen == False:
                    notebook.forget(notebook.select())
                else:
                    pass
        log('deleted current tab', call='TABS')
    except:
        mainwindow.quit()

def saveAsFile(*args):
    global notebook
    global extension
    global filepath
    filepath = asksaveasfilename(defaultextension="",filetypes=[("All Files", "*.*"),("Text Files", "*.txt"),("Ada"         ,[".adb",".ads"]),("Bash"        ,[".sh",".csh",".ksh"]),("Batch"       ,[".cmd",".bat"]),("BrainFuck"   ,[".b",".bf"]),("C"           ,[".c",".h"]),("CMake"       ,[]),("CoffeeScript",[".coffee",".cson",".litcoffee"]),("CSS"         ,[".css"]),("C#"          ,[".cs",".csx"]),("C++"         ,[".cc",".cpp",".cxx",".c++",".hh",".hpp",".hxx",".h++"]),("Dart"        ,[".dart"]),("Delphi"      ,[".dpr"]),("Dockerfile"  ,[".dockerfile"]),("Fortran"     ,[".f",".f90",".f95"]),("Go"          ,[".go"]),("Groovy"      ,[".groovy",".gvy",".gradle",".jenkinsfile"]),("Haskell"     ,[".hs",".lhs"]),("HTML"        ,[".htm",".html"]),("Java"        ,[".java",".jar",".class"]),("JavaScript"  ,[".js",".cjs",".mjs"]),("JSON"        ,[".json"]),("Kotlin"      ,[".kt",".kts",".ktm"]),("Lisp"        ,[".lsp"]),("Lua"         ,[".lua"]),("MATLAB"      ,[".m",".p",".mex",".mat",".fig",".mlx",".mlapp",".mltbx"]),("MakeFile"    ,[".make",".makefile"]),("NASM"        ,[".asm",".asm",".inc"]),("Objective-C" ,[".mm"]),("Perl"        ,[".plx",".pl",".pm",".xs",".t",".pod"]),("PHP"         ,[".php",".phar",".phtml",".pht",".phps"]),("Powershell"  ,[".ps1"]),("Python"      ,[".py",".pyi",".pyc",".pyd",".pyo",".pyw",".pyz"]),("R"           ,[".r",".rdata",".rds",".rda"]),("Ruby"        ,[".rb"]),("Swift"       ,[".swift"]),("SQL"         ,[".sql"]),("Tcl"         ,[".tcl",".tbc"]),("TypeScript"  ,[".ts",".tsx"]),("Vim"         ,[".vim"]),("YAML"        ,[".yaml",".yml"]),])
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        extension[current_note()] = "."+filepath.split(".")[-1]
        tabfmt[current_note()] = "."+filepath.split(".")[-1]
        variable = int(current_note())
        text = note[variable].get(1.0, tk.END)
        output_file.write(text)
        log('saved file {}'.format(filepath), call='FILES')
    notebook.tab(frames[int(current_note())], text = filepath.split("/")[-1]+"  ")
    openedfiles[current_note()] = filepath
    note[current_note()].config(language=identify(filepath.split("/")[-1]))
    note[current_note()].update()
    root.update()

def saveFile(*args):
    global notebook
    global extension
    variable = int(current_note())
    if openedfiles[variable] == "":
        saveAsFile()
    else:
        with open(openedfiles[variable], "w") as output_file:
            extension[current_note()] = "."+openedfiles[variable].split(".")[-1]
            tabfmt[current_note()] = "."+openedfiles[variable].split(".")[-1]
            text = note[variable].get(1.0, tk.END)
            output_file.write(text)
            notebook.tab(frames[variable], text = openedfiles[current_note()].split("/")[-1]+"  ")
            log('saved file {}'.format(filepath), call='FILES')

def openFile(*self):
    global extension
    global filepath
    if notebook.select() == "":
        newTab()
    variable = current_note()
    filepath = askopenfilename(defaultextension="*.*", filetypes=[("All Files","*.*"), ("Text","*.txt"),("Ada"         ,[".adb",".ads"]),("Bash"        ,[".sh",".csh",".ksh"]),("Batch"       ,[".cmd",".bat"]),("BrainFuck"   ,[".b",".bf"]),("C"           ,[".c",".h"]),("CMake"       ,[]),("CoffeeScript",[".coffee",".cson",".litcoffee"]),("CSS"         ,[".css"]),("C#"          ,[".cs",".csx"]),("C++"         ,[".cc",".cpp",".cxx",".c++",".hh",".hpp",".hxx",".h++"]),("Dart"        ,[".dart"]),("Delphi"      ,[".dpr"]),("Dockerfile"  ,[".dockerfile"]),("Fortran"     ,[".f",".f90",".f95"]),("Go"          ,[".go"]),("Groovy"      ,[".groovy",".gvy",".gradle",".jenkinsfile"]),("Haskell"     ,[".hs",".lhs"]),("HTML"        ,[".htm",".html"]),("Java"        ,[".java",".jar",".class"]),("JavaScript"  ,[".js",".cjs",".mjs"]),("JSON"        ,[".json"]),("Kotlin"      ,[".kt",".kts",".ktm"]),("Lisp"        ,[".lsp"]),("Lua"         ,[".lua"]),("MATLAB"      ,[".m",".p",".mex",".mat",".fig",".mlx",".mlapp",".mltbx"]),("MakeFile"    ,[".make",".makefile"]),("NASM"        ,[".asm",".asm",".inc"]),("Objective-C" ,[".mm"]),("Perl"        ,[".plx",".pl",".pm",".xs",".t",".pod"]),("PHP"         ,[".php",".phar",".phtml",".pht",".phps"]),("Powershell"  ,[".ps1"]),("Python"      ,[".py",".pyi",".pyc",".pyd",".pyo",".pyw",".pyz"]),("R"           ,[".r",".rdata",".rds",".rda"]),("Ruby"        ,[".rb"]),("Swift"       ,[".swift"]),("SQL"         ,[".sql"]),("Tcl"         ,[".tcl",".tbc"]),("TypeScript"  ,[".ts",".tsx"]),("Vim"         ,[".vim"]),("YAML"        ,[".yaml",".yml"]),])
    if filepath == "":
        filepath = None
    else:
        try:
            extension[current_note()] = "."+filepath.split(".")[-1]
            tabfmt[current_note()]= "."+filepath.split(".")[-1]
            print(note)
            note[int(current_note())].delete(1.0,END)
            note[current_note()]["language"] = identify(filepath.split("/")[-1])
            file = open(filepath)
            content=file.read()[:-1]
            note[variable].insert(1.0,content)
            openedfiles[variable] = filepath
            file.close()
            notebook.tab(frames[variable], text = filepath.split("/")[-1]+"  ")
            note[current_note()].config(language=identify("."+filepath.split(".")[-1]))
            log('opened file {}'.format(filepath), call='FILES')
        except UnicodeDecodeError as uce:
            log('({}) {}'.format(type(uce).__name__, uce), call='FILES')
            showerror(type(uce).__name__, uce)

def select_all(event):
    note[current_note()].tag_add(SEL, "1.0", END)
    note[current_note()].mark_set(INSERT, "1.0")
    note[current_note()].see(INSERT)

def newTab(*args):
    #pygments.lexers.installers
    global var
    global notebook
    frames[var+1] = ttk.Frame(notebook)
    note[var+1] = ''
    note[var+1] = CodeEditor(frames[var+1],blockcursor=data.configuration['Looks']['Font']['BlockCursor'],width=40, height=100, autofocus=True, insertofftime=0, padx=0, pady=0, font=data.font, highlighter = default_highlight)
    note[var+1].pack(fill="both", expand=True)
    note[var+1].lexer = eval("Lexers."+data.configuration['Looks']['InitialSyntax']+'.'+data.configuration['Looks']['InitialSyntax'])
    font = tkfont.Font(font=note[var+1]['font'])
    note[var+1].config(tabs=font.measure('    '))
    notebook.add(frames[var+1], text='Untitled  ')
    nexttab()
    openedfiles[int(var)+1] = ""
    extension[current_note()] = ".*"
    note[var+1].bind('<Control-Tab>',nexttab)
    note[var+1].bind('<Return>', auto_indent)
    note[var+1].bind("<Control-a>",select_all)
    #note[var+1].lexer = NSIS.NSIS
    var = var + 1
    tabfmt[current_note()] = '.py'
    log('new tab added', call='TABS')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

notebook = widgets.Notebook(root)
notebook.grid(sticky=N + E + S + W)
notebook.bind("<B1-Motion>", Tab_reorder)

nwtb = ttk.Button(notebook, text='New Tab', command=newTab, style='primary.Link.TButton')
nwtb.place(relx=0.44,rely=0.5,anchor="center")

opfl = ttk.Button(notebook, text='Open File', command=openFile, style='primary.Link.TButton')
opfl.place(relx=0.55,rely=0.5,anchor="center")

greet = tk.Label(notebook,text='Good {}, {}'.format(greet_time(), getpass.getuser()), font='Consolas 30')
greet.place(relx=0.5,rely=0.4,anchor="center")

def nexttab(*args):
    try:
        notebook.select(current_note()+1)
    except:
        notebook.select(0)

extension[current_note()] = ".*"

btn = ttk.Button(mainwindow,text = 'NEW')
btn.place(anchor='ne')

if len(sys.argv) >= 2:
    variable = current_note()
    if os.path.isfile(sys.argv[1]):
        extension[current_note()] = "."+filepath.split(".")[-1]
        note[variable].delete(1.0,END)
        file = open(filepath,"r")
        note[current_note()]["language"] = identify(filepath.split("/")[-1])
        note[variable].insert(1.0,file.read())
        openedfiles[variable] = filepath
        file.close()
        notebook.tab(frames[variable], text = filepath.split("/")[-1]+"   ")
        note[current_note()].config(language=identify("."+filepath.split(".")[-1]))

root.add(notebook, before=termframe, height=450)

class Generate:
    def copy(__widget__):
        try:
            __widget__.event_generate("<<Copy>>")
        except:
            pass
    def cut(__widget__):
        try:
            __widget__.event_generate("<<Cut>>")
        except:
            pass
    def paste(__widget__):
        try:
            __widget__.event_generate("<<Paste>>")
        except:
            pass

def texteditmenu(event):
    _widget = event.widget
    tkTextmenu.entryconfigure("Cut",command=lambda: Generate.cut(_widget))
    tkTextmenu.entryconfigure("Copy",command=lambda: Generate.copy(_widget))
    tkTextmenu.entryconfigure("Paste",command=lambda: Generate.paste(_widget))
    tkTextmenu.tk.call("tk_popup", tkTextmenu, event.x_root, event.y_root)

def startfind(*args):
    widgets.Find(mainwindow, note[current_note()])

def startreplace(*args):
    widgets.Replace(mainwindow, note[current_note()])

def toggle_searchbox(*args):
    global sboxshow
    print(sboxshow)
    if sboxshow:
        searchbox.place_forget()
        sboxshow = False
    else:
        searchbox.place(relx=0.4,rely=0.1)
        searchbox.focus_set()
        sboxshow = True

def exec_command_in_searchbox(event):
    cmd = searchbox_entry.get()
    try:
        if cmd[0] == '!':
            exec(cmd[1:])
        elif cmd[0] == '$':
            os.system(cmd[1:])
        else:
            cmd = cmd.lower()
            print("command_pallete.{}['{}']".format(cmd.split()[0], cmd.split()[1]))
            exec(eval("command_pallete.{}['{}']".format(cmd.split()[0], cmd.split()[1]))+'()')
        toggle_searchbox()
    except:
        toggle_searchbox()

class command_pallete:
    file= {
        "": None,
        "open": "openFile",
        "save": "saveFile",
        "saveas": "saveAsFile",
        "close": "deltab",
        "quit": "sys.exit",
    }

#special widget: internal command processor
searchbox = ttk.Frame(mainwindow, borderwidth=3)
searchbox_text = ttk.Label(searchbox, font='consolas 15', text = '>')
searchbox_text.pack(side='left')
searchbox_entry = ttk.Entry(searchbox, font='consolas 15', width=25)
searchbox_entry.pack(side='right')
sboxshow=False
searchbox_entry.bind('<Return>',exec_command_in_searchbox)

tkTextmenu = tk.Menu(root, tearoff=0)
tkTextmenu.add_command(label="Cut")
tkTextmenu.add_command(label="Copy")
tkTextmenu.add_command(label="Paste")

notebook.bind("<Double-Button>", newTab)
notebook.bind("<ButtonRelease-2>", smartdeletetab)
mainwindow.bind_all(data.configuration['Key Bindings']['Save'], saveFile)
mainwindow.bind_all(data.configuration['Key Bindings']['New'], newTab)
mainwindow.bind_all(data.configuration['Key Bindings']['Close'], deltab)
mainwindow.bind_all(data.configuration['Key Bindings']['Open'], openFile)
mainwindow.bind_all("<Control-F5>",runfile)
mainwindow.bind_all(data.configuration['Key Bindings']['Run'], runconf)
mainwindow.bind_all(data.configuration['Key Bindings']['Open cmd'], opencmd)
mainwindow.bind_all("<Key>", update)
mainwindow.bind_all("<Button-1>", update)
mainwindow.bind_all('<Control-Tab>', nexttab)
notebook.bind_all('<Control-Tab>', nexttab)
mainwindow.bind_all(data.configuration['Key Bindings']['Fullscreen'], fullscreen)
mainwindow.bind_class("Text", "<Button-3><ButtonRelease-3>", texteditmenu)
mainwindow.bind('<Control-f>', startfind)
mainwindow.bind('<Control-h>', startreplace)
mainwindow.bind('<F1>', toggle_searchbox)
mainwindow.bind('<Control-P>',toggle_searchbox)
mainwindow.config(menu=None)
mainwindow.after(1000, exec('datafile = open(PATH+"/DATA/runner.confscript").read()'))
log('binded all keystrokes')
log('starting main window')
execute((xtmgr.tasks.before_mainloop))
try:
    mainwindow.mainloop()
except Exception as e:
    log('({}) {}'.format(type(e).__name__, e), call='ERROR')
    showerror(type(e).__name__, e)
mainwindow.quit()
configs.close()
execute((xtmgr.tasks.before_configs_save))
open(PATH+'/DATA/configure.yaml','w+').write(yaml.dump(data.config))
try:
    shutil.rmtree(tempfile.gettempdir()+'/WhirlEdit')
    log('removed TEMP/WhirlEdit folder')
except:
    pass
log('Exiting program')
print('** See you later **')
sys.exit()
