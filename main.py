__version__ = 'v3.4 (Stable)'
import time
start = time.time()
import utils as txtutils
import zlib
import os
import yaml
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import tkinter.font as tkfont
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from tkinter.messagebox import askyesnocancel
import subprocess
import shutil
import tkinter
import zipfile
import tempfile
from wday import read
from confscript import read as cfsread
from confscript import dump
from tkcode import CodeEditor
import webbrowser

TEMP = tempfile.gettempdir()
logx = ''
if os.path.isdir(TEMP+'/WhirlEdit/'):
	pass
else:
	os.mkdir(TEMP+'\\Whirledit\\')
	#logfile=os.open(TEMP+'/Whirledit/logs.txt', os.O_RDWR|os.O_CREAT)

logfile = open(os.path.abspath(TEMP+'\\Whirledit\\logs.txt'),'w+')
logfile.write('')

def logCALL(message, call="INTERNAL"):
	logs = '{} [{}]: {}'.format(round(time.time()-start,2),call,message)
	logx += logs+'\n'
	logfile.writelines(logs+'\n')
	print(logs)

def reorder(event):
    try:
        index = notebook.index(f"@{event.x},{event.y}")
        notebook.insert(index, child=notebook.select())

    except tk.TclError:
        pass

class Notebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "Notebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        ...
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", file='./DATA/icons/close.n.png'),
            tk.PhotoImage("img_closeactive", file='./DATA/icons/close.n.png'),
            tk.PhotoImage("img_closepressed", file='./DATA/icons/close.a.png'),
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"),)
        style.layout("Notebook", [("Notebook.client", {"sticky": "nswe"})])
        style.layout("Notebook.Tab", [
            ("Notebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("Notebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("Notebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("Notebook.label", {"side": "left", "sticky": ''}),
                                    ("Notebook.close", {"side": "right", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

configuration = """
Key Bindings:
  Close: <Control-w>
  Fullscreen: <F11>
  New: <Control-n>
  Open: <Control-o>
  Open cmd: <Control-Shift-t>
  Run: <F5>
  Save: <Control-s>
Logs:
  Logging: false
Looks:
  Font:
    BlockCursor: true
    Font: Consolas
    Size: '12'
  Icons:
    Theme: fluent.dark
  InitialSyntax: python
  Scheme:
    Default: azure-modified
    Folder: ./DATA/Schemes/
  Theme:
    Default: forest-dark.whTheme
    Folder: ./DATA/Themes/
  WindowTitle: WhirlEdit

"""
try:
	configuration = (yaml.safe_load(open('./DATA/configure.yaml').read()))
except Exception:
	configuration = (yaml.safe_load(configuration))

def logFAKE(message, call='INTERNAL'):
	logs = '{} [{}]: {}'.format(round(time.time()-start,2),call,message)
	logfile.writelines(logs+'\n')

if configuration['Logs']['Logging']:
	log = logCALL
else:
	log = logFAKE

openedfolders = []

highlight = {
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
			"HTML"        : [".htm",".html"],
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
			}

nothing = [1,0,1,1,1,1]


class data:
	logo = b'x\xda-V\xc7\x1a\xa20\x10~ \x0f\x02\x02\xcaa\x0f\t\xbd7A\xe0&-A\xaa\x14\x01\x9f~q\xbf\r\x04\xc8\xf4\xf9g\x92\x8f*\x84\xb6\xb7\x12\xba\x8czp\x0c\xcb\x0f\xb0\x18\xa0\xe3Kv\x8f\x07\xacy`\xfe\xde\x8a#\x87\xedO\x00\xca9\xbc\x07"\x00\x86\xec\xf0\xe7\r\xc3\x9f\x18\x90\xbeA\x9d\xf3@\xbf\xda\x8a]\x1fk\xa3\x0f\xc4-\xf0\x82m\xc8\x8aW\xcf*!\x99\xe7\xf7\x80t.\xdc9\xe5\xd7I}\xca\xb8\xb6\x04\x97\xc0\xaa\xaf\xebU?]\xaco\x98G\xe1\xf9\xff\xa0\xc2&\x89\xb8sy\xb5\xbf\x13\xb3\xa4\xed\xcd\xe0\xd76i\x93\xc5y\xd1\x17L\x17\xf26\xa5"c\xdf?\x87\xec\xa9\x1b\xd8G3<#m\xcf:\x8f\xc8\x15\xe6T\xbe\xedW\x7f-.3\x05Ql\x1f:\xcc#l\x8e;y\xb6\xc3;\xa6\xacW\xd6i{\xc2\xbb\xb5\x18J\xde\xc3z\xc5\x9cs\'~~/\t\x95\xb7\xdc\'%\xad{\xc0\x1c|\xeb\x9b]~\xf6jO\xf4\xa4\x83\xc6\xca\xb8\x8fm\x01Q\x87\x7f\xe3I\xcd\xeda\xb3\xfc\xde\xcez\xd1\r?}\x12\xba\x81\x1d5Lz\xf8\xfe\xad\xe9\x93\xf3"\x1a\xcdOt\xbf\xfe\xc5J\xe2\xf8\xc1\xf7o\x1dA\xbbC\xb0\xda\x00\x94*\xc4\x8b\xe7\x15.\x97\xea\xa0\xfb\xa8\xd7e\xafN\xc0\xc1_\x0f\xde\xcaK\x07\xcf\xee\xbc\x9ay\xfc\xe4\xddF\xc1\xe8\xa0\xfb\xf1l\xae\xf59_\xe1k\xab\xe2\xc5\xf2j2\xa8\xfaA[\xe1\x87\x86\x9eR\xec\xf5\xa0\xbb\xa4\xd7\xf8\xfd\xa0\x03\x99?\xf9h2\xbdY\xcf\xdd\x9c\xa4\xf6\x80\xf4x4\x9b?\x7f+\xf9|\x83\xc3\xf7\n\xcd\x16A\xf9\x05=\xbbr\xa1\xd3\x03\x98-.\x0fN.\xdc\xe8\n\x8d\x06"\xb8\xd4\x85=\x81x\xe1\xec\xbb\x8b\r\x12\xf5\x90}\xb68\xb8\xc6\x9e\xa4c\xbe\x1f\r\x88\x1dTeG,\xa1\x98a\xc9o\xdc!\x9f\xaa\xecc\xad\xc3\xb2\xef\xebd\xf0\xd3\xa8\xefh\xb1xz1^\x88\xb6\x85\xe0@\x19\xac&\x7f\xc4\xc6\xd7\xa3\xf1\x9b\x1e\xb6\xd1aK\xdf$\xbf\xde\x8ex\xf1\x91\x97K&\xc3/\xd7*\x9e\xcc_\xec>1\x1b\xf7\xech\x18\x97\xb0\x04q3\xef?\x90\xa7\xa3S\xcc\xaf\xf9\xd3Y5\xb3u\xe1|\x01G\x96.l\xbf\x00+\x15\x9c\xbew@\xdf\x9ex\xa5\x02\xe8\x19\xf8\x87I\x056\xd7\x8b\xd9h\xb3\xd4\xb2:\xf0X\xc3\xe7\xb8\x1fXb\xc4<\xb0\xa5\x95\x07\xfe/x\xe4\xf6\xcb\xdb\x0bn\xf1\xe6\xa9%8\xf2\xe7E\xca_\x8f\xdc\xdc-}o\xb9\x90\xe2\x98\x8d\xbd\x1b\x1d\xf0\xd9j\x03^>\xaf\xdb\xb0\xfa\xf5d\xe0\\+\xdd9\x1bq"d.D+\x90&\xcaC\xa7\xc4\x85\xe9\xbc\x99L\xb4\x016\xf1\x0f\xbc\x10t\xba_\xdd|p\x8e`#f\xc0\xbb\xb2\x08\x86o\xbc\xa9\x99?\xbdu>\x9b-\x10j\xaf*\x9e\x8f\xcdy`\x7f\xc4\xb3e\x97\xc7\xaf>\xe8\xa8\xcf\x8ae\x8c\xa5cs&\xe8\x03\xa0\xd1B\xcby\xfd\xea\xebZWvm`\x81\x8f\x9a\x022\x1f\x8f\x9e\xb1\x80\xf5\x9c\\\xc8qh\xf3[?X\xed\x15\xab\xff\xea\xed\x07\x84[\xb9\x17\xdf\x1d\xe6\x1d\xcd\xfd\n\xe0J#LPn\xb3\x13{=\x9b\xbcz\r6-\xef\xb7$\xac\xf9xw\x80,\x9cac#\xc7\x0b\xbf\x1b\xfd;\x15\xa4\\\xd2\xec`\x05\xf1\xcaOvd87\x8e\x16\x97+R\x15:\x9d\x1f(\x88njz^n\xc8\xcd\xb9\xacT\xf7\xce\x8ai|J\xcf\x1d\xbf\xd8I\xc4P\xfbM\xa6\xec\x8ek\xaa\xear*8z\xb3\xb4;\x87=\n\x94 \x0b\xd7\xf7x\xeeW\x81\xe9?\x07\xcc\xbf\xb3\xc5\xc4~\xe0\xc1P~\x15\xd7|\x08C\xe8y\xb2)l<\x8d\r?\xca\xc6KN\xcd\xd1\x11\xa8\xfb\x92\xdcC\xf9.\xa5\xf2\x96QuP\xf3\xecu\xf9\x7fQd&Q\t%e[\xde\xb6i}c\x9d\xad\xcco\xe7\xdbw\xfa\xf2]\\~\x00\xc1\x07u\x10\xa4\xe6\x85\xcau\xe9\xb9\x9b\xdd\x93\x9a\xa2\x84\x00\x9f\xf0\x9d>\x98\xaa\xd6D\xdb\xbf\xd3W\xf7!\x87\x9f\xd8\xce\xc7\xa7X\x13\xc1xo\xf8\xb2\xae\x19\xc1:\t\x82\x10\xd4\x8bm6}\xfff\x9f_\x9d\xf3D\xb7a\x0c\x98*^\x88\xba\xaa\xf2\xf70d\x1b.\x9c\x06]3\xfd\xa6\x91\xbb\x9e\xac\xf8\xe7\x1b\xc32Q\xc3\xf4\xe1De\xf3\xa8\xd9Mo\xe8SI\xc2\xafR\xd7w\xe4\xb5\x85\xeb\x02u3q\x88\x9c\x1d\x116\xc4\xaeX\x1a\x84\xd6\xe2\xde\xa4\xe4\xa8*\xa5\xde\x1f\x8c\tLJjB?,\xd0\xeb\xbc\x03\xa46\xc1+\\\xeb\x9c~\xf7\x91\xaa\x81\xf2)\xfa\xac\xce\x17\xe1b\x14V2u\x157\xc63+ScV\xa5\xaa?~J8\xe8\xba+y\x95u\xca)C\\\xba\xea\xbd\xac^\xfc\xb9\xeb\x80\xcd\x11f(\n\xd7\xf9Z>\xd3\xa2\x9e\x88\xbc\x13vi\x86*\xe7\x0c\xea\xc9\xac\xeb\xd8O\x06f\x12\xda,\xc6\x8ac\x94\xaaX<\xabe\x0f\xc0\xbd9\x85\xb6F\xb0\x18D\x17\x02\\\xd8\x8a\xbf\x92\xb3\xa6,\r}3\x13\xe3}\xca\xe6\x131\xce\x11\xdc\xebXE\x8e\xcf\x04\xfb\xbe\x08\xc5\'\xa2\x02\xa7\x96\x0cj]KA\xd3dlV\xb2\x17ZJ\xdea\xc5\x8f\x1a$*\xa6\xf8 \xfa\xc5=7\xd7Z\x04W\\+7Ou\xef}7\xf2\xaa(\x9d\x0b\tqr\xa8|/\\[\xbd_kh\x8a\xb6\xa1\xcc\xc4I\xa8\x05\x8a\xb5\xe2\xf1\xbd\x85f[\xd9B\xf4%\xd1\x90\'j\xcf\xd5\xe6\xb3\xbee\xe4\x94]\xa5\x01F\xd7\xb2\x89\xbf\xaaa2X4\xe9A\x91j\x85\xb1\xbf\xecw\x9a\x13\xe7\x06\xb5\xa9\xd0i\xfb\xd3\x9d\x1b\xed\xb9D\xd4m\x01\x1fF\x144\xa6\xbb\xee\xd7F\xb8\xb9T\xb93\x01\x11YNT\xb8\xb2o\xf4\xeen\xc2D\x8d\xd7*0\xe9\x7f\xf6 \xb33w\rNl\xfc\n\xa9\xb3\xcd\x12\xd4X<\xe7=\x11\x01\xe5\xf3\xba\xb7R?\xd2\xd7\x0bp{\x9c\x80\x12Y\xeb\xbemY\x0b\x91\x02\x86K$\xf5^\'\xd5\x16\x7f+\xd1=\xe6\xfd\xe19\xd9.\x18\xd2\xee)\x01G:\xd5[I\xfd\xf2\x8e\xbe\xa0\'\x9b\xecR,\xad\xcf/\xc2\xe2\xf0\x97\x8f\xff>\xc3\x80\xef\xb4\x9a\xefw\x8f\xa1R\xfb\x84=\x8fdo!\xf7\x84\x89Xj4\xd6: \xdf/\xa26\xf4AQ\xad)x\xec\xef\xc9\xe4N\xe7X&\x9d"\xf1\xec\xec\xbb\x83\x98\xb6\x17\xf9,\x9a\x1b\xa0\xa9\x87X\xecz\xc9.\xc8BO\xba\xb9\x14\xb4\xd2)\xae\x0fz/\xb5\xef\xee\xbeG\xfc\xa9.ZN\x1a\xdb`p\xeaG?~\xc8\x0b\x0cr\xf8A\xfb\xddEc\xaa\xb3ch`{xJ\x1e\n\xcaW\xc3\xf6\xe3\xbc\xc9\xb3\xb7\xb4L\xf1\x88vJ\xb9\xeb\xe1\xc0\x16\xb36*H*\xd2NL\xf6d\xaf4\xa1n\xda\xe23\xd3\x98\x0b\xd3\x10\xd4\x86\x10\x85\xeb\xe8\x93/\xf6r\xab\xcc\x9b\x93i98\xbd?e\xf2Y$s\xf5\xf34\x1a\xa9\xec\xf7\xa3\x02\xfc \xb4=\x9d\xe1cU\xfd\xf3\x17\xe8\xaa\xff\xa1'
	font = "{} {}".format(configuration['Looks']['Font']['Font'],configuration['Looks']['Font']['Size'])
	isBlockcursor = configuration['Looks']['Font']['BlockCursor']
	config = configuration

def about(*args):
	log('opening about')
	def nothingmod(pos,val, ext=None):
		nothing[pos] = val
		a.destroy()
	if nothing[4] == 1:
		a = tk.Toplevel(thisroot)
		nothing[4] = 0
		a.wm_attributes("-topmost",1)
		a.title('Whirledit')
		a.resizable(False,False)
		a.iconbitmap(r"./DATA/icons/favicon.v3.ico")
		a.geometry("300x250")
		z = Label(a, image=img100x100)
		z.pack(pady=5,padx=5)
		b = Label(a,text='WhirlEdit',font='Consolas 20')
		b.pack()
		c = Label(a,text=__version__,font='Consolas 10')
		c.pack()
		d = Label(a,text='\nWritten in Python\nby Whirlpool-Programmer\n',font='Consolas 15')
		d.pack()
		e = ttk.Button(a,text='GitHub', command=lambda:webbrowser.open('http://Whirlpool-Programmer.github.io/software/WhirlEdit'))
		e.pack()
		tk.Label(a,text=' ').pack()
		a.protocol("WM_DELETE_WINDOW", lambda:nothingmod(4,1))
	else:
		pass

def fullscreen(*args):
	if nothing[1] == 0:
		log('on',call='FULLSCREEN')
		thisroot.wm_attributes("-fullscreen",1)
		nothing[1] = 1
	else:
		log('off',call='FULLSCREEN')
		thisroot.wm_attributes("-fullscreen",0)
		nothing[1] = 0

def set_syntax(lang):
	note[current_note()].config(language=lang)
	log(lang,call='SYNTAX')

def togglesetti(*args):
	global nothing
	if nothing[5] ==0:
		splitter.forget(settipaneframe)
		nothing[5] = 1
	else:
		splitter.add(settipaneframe,before=root,width=220)
		splitter.forget(runnerpaneframe)
		splitter.forget(filespaneframe)
		splitter.forget(lookspaneframe)
		nothing[5] =0

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
	if nothing[2] ==0:
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

tabfmt = {}

def update(*args):
	thisfile = ""
	if openedfiles[current_note()] == '' or openedfiles[current_note()] == ' ':
		thisfile='None'
	else:
		thisfile = openedfiles[current_note()]
	root.update()
	cursyntax.set(identify(tabfmt[current_note()]))
	fdir = "/".join(openedfiles[current_note()].split("/")[:-1])
	line = note[current_note()].index(tk.INSERT).split('.')
	note[current_note()]['font'] = data.config['Looks']['Font']['Font']+" "+data.config['Looks']['Font']['Size']
	note[current_note()]['blockcursor'] = data.isBlockcursor
	status['text'] = "File: {} | Line {}, Column {}".format(thisfile,line[0],line[1])
	if fdir in openedfolders:
		pass
	else:
		framed.add(fdir)
		openedfolders.append(fdir)
		log('added {}'.format(fdir), call='FOLDER')

def openthisfile(event):
	global extension
	global filepath
	if notebook.select() == "":
		newTab()
	item_id = event.widget.focus()
	item = event.widget.item(item_id)
	values = item['text']
	if os.path.isfile(values):
		variable = current_note()
		filepath = values
		extension[current_note()] = "."+filepath.split(".")[-1]
		note[variable].delete(1.0,END)
		file = open(filepath,"r")
		note[current_note()]["language"] = identify(filepath.split("/")[-1])
		note[variable].insert(1.0,file.read())
		openedfiles[variable] = filepath
		file.close()
		log('opened {}'.format(filepath, call='FILE'))
		notebook.tab(frames[variable], text = filepath.split("/")[-1]+"   ")
		note[current_note()].config(language=identify("."+filepath.split(".")[-1]))

def changekeybind(*args):
	def getit__(index):
		data.config['Key Bindings'][theselabels[i]['text']] = theseentries[i].get()
	menu = tk.Toplevel(thisroot)
	theseframes  = {}
	theselabels  = {}
	theseentries = {}
	listss = []
	for i in data.config['Key Bindings'].keys():
		listss.append(i)
	for i in range(len(data.config['Key Bindings'].keys())):
		theseframes[i] = ttk.Frame(menu)
		theselabels[i] = tk.Label(theseframes[i],text=listss[i])
		theselabels[i].pack(side='left',fill='x')
		theseentries[i] = ttk.Entry(theseframes[i])
		theseentries[i].insert(0, data.config['Key Bindings'][listss[i]])
		theseentries[i].pack(side='right',fill='x')
		theseentries[i].bind('<Return>',lambda i=i:getit__(i))
		theseframes[i].pack(fill='x',side='bottom')
	tk.Label(menu,text='Info: Change the entries and hit <Return> to save').pack()
	menu.mainloop()

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
        							fg="#101010",
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("Consolas", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
    log('added {}'.format(str(widget)),call='TOOLTIP')


class Settings(object):
	def savechangesSETTINGS(self):
		data.config['Looks']['Theme']['Folder']  = self.themeFolder.get()
		data.config['Looks']['Theme']['Default'] = self.themeName.get()
		data.config['Looks']['Scheme']['Folder'] = self.schemeFolder.get()
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

class runnerpane(object):
	def __init__(self,master):
		frame = tk.Frame(master)
		self.button = ttk.Button(frame,text='Open CMD', command = lambda:opencmd())
		CreateToolTip(self.button, text='open Windows Command Processor (cmd)\nin the current directory')
		self.rubbish0 = tk.Label(frame,text=' ')
		self.rubbish0.grid()
		self.l1 = tk.Label(frame,text='  ')
		self.l1.grid(row=2,column=0)
		currun = StringVar()
		self.runners = ['This runner']
		self.rns = tk.Menu(frame)
		for i in getConfs():
			if i != "@":
				self.rns.add("command",label = i, command = lambda i=i: runnerConf(i))
		self.chooserunner = ttk.Menubutton(frame, menu=self.rns,text = 'Run current file with')
		CreateToolTip(self.chooserunner, text="Choose the runner to run\nthe currently opened\ntab..")
		self.chooserunner.grid(row=2,column=1, sticky='nsew')
		self.rubbish1 = tk.Label(frame,text=' ')
		self.rubbish1.grid()
		self.button.grid(row=4,column=1)
		self.rubbish2=tk.Label(frame,text=' ').grid()
		self.newrunbtn = ttk.Button(frame,text = 'New Runner',command=lambda:newrunner())
		self.newrunbtn.grid(row=6,column=1)
		CreateToolTip(self.newrunbtn, text='Create a new runner \nand save to\nrunners file')
		frame.grid()

class lookspane(object):
	def configsave(self,*args):
		if self.g.get() =='':
			pass
		else:
			thisroot.title(self.g.get())
			data.config['Looks']['WindowTitle'] = thisroot.title()
		data.font = self.i.get()
		data.config['Looks']['Font']['Font'] = "\ ".join(data.font.split()[0:-1])
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
		for i in os.listdir(configuration['Looks']['Scheme']['Folder']):
			if i.lower().endswith('.json'):
				curscheme_values.append(i[:-5])
		self.b = ttk.OptionMenu(frame, self.curscheme, *curscheme_values, command = lambda a='s':note[current_note()].config(highlighter = configuration['Looks']['Scheme']['Folder']+self.curscheme.get()+'.json'))
		self.d = tk.Label(frame,text='Syntax')
		CreateToolTip(self.b, text='Select The color-scheme\nto use..')
		self.d.grid(row=2,column=0)
		self.e = tk.Label(frame,text='Scheme')
		self.e.grid(row=3,column=0)
		cursyntax = StringVar()
		languages = ['Choose']
		for i in highlight.keys():
			languages.append(i)
		self.c = ttk.OptionMenu(frame, cursyntax, *languages,command=lambda name="__main__": note[current_note()].config(language=cursyntax.get()))
		self.c.grid(row=2,column=1, pady=5)
		CreateToolTip(self.c, text='Select the programming language\nsyntax to use')
		self.b.grid(row=3,column=1,pady=5)
		self.f = tk.Label(frame,text='Window Title')
		self.f.grid(row=4,column=0,pady=5)
		self.g = ttk.Entry(frame,width=20)
		CreateToolTip(self.g, text='Add a new window title')
		self.g.grid(row=4,column=1,pady=5)
		self.h = tk.Label(frame,text='Font:')
		self.curfont=StringVar()
		self.curfont.set('{} {}'.format(configuration['Looks']['Font']['Font'],str(configuration['Looks']['Font']['Size'])))
		self.j = tk.Label(frame,text='Font')
		self.j.grid(row=5,column=0,pady=5)
		self.i = ttk.Entry(frame, text= self.curfont.get())
		CreateToolTip(self.i, text='Write the font to be used\nsyntax: "NAME SIZE"')
		self.i.insert(0,self.curfont.get())
		self.i.grid(row=5,column=1, pady=5)
		self.k = tk.Label(frame,text='Block Cursor')
		self.k.grid(row=6,column=0, pady=5)
		self.isBlockcursor = BooleanVar()
		self.isBlockcursor.set(data.config['Looks']['Font']['BlockCursor'])
		self.j = ttk.Checkbutton(frame, variable=self.isBlockcursor)
		CreateToolTip(self.j, text='Shall you use Block Cursor\ninstead of normal "thin" one?')
		self.j.grid(row=6, column=1, sticky='w')
		rubbish1 = tk.Label(frame)
		rubbish1.grid()

		self.configconfirm = ttk.Button(frame,text="Save", command=self.configsave)
		self.configconfirm.grid(row=8,column=0)
		frame.grid(sticky='NEWS')


class PathView(object):
	def add_openfold(self):
		the_Folder = askdirectory()
		self.add(the_Folder)
		log('added '+the_Folder,call='FOLDER')
	def add(self,path):
		abspath = os.path.abspath(path)
		self.insert_node('', abspath.split('\\')[-1], abspath)
		self.tree.bind('<<TreeviewOpen>>', self.open_node)
	def __init__(self, master, paths):
		main = tk.PanedWindow(master,handlesize=5,orient=VERTICAL)
		main.pack(expand=True, fill='both')
		tabspane = tk.Frame(main)
		listbox = tk.Listbox(tabspane)
		listbox.pack(expand=True,fill='both')
		#tabspane.pack(fill=BOTH,expand=1)
		frame = tk.Frame(main)
		nf=tk.Frame(frame)
		self.newfilebtn = tk.Button(nf, relief='flat', image=projectBar_icon_newfile, borderwidth=0, command= lambda:newTab())
		self.newfilebtn.grid(row=0, column=0, ipady=5, ipadx=5)
		self.newfoldbtn = tk.Button(nf,relief='flat', image=projectBar_icon_newfold, borderwidth=0, command = lambda:self.add_openfold())
		self.newfoldbtn.grid(row=0, column=1, ipady=5, ipadx=5)
		self.closetabtn = tk.Button(nf, relief='flat', image=projectBar_icon_closefi,borderwidth=0, command=lambda:deltab())
		self.closetabtn.grid(row=0, column=2, ipady=5, ipadx=5)
		CreateToolTip(self.newfilebtn, text='New Tab')
		CreateToolTip(self.newfoldbtn, text='Add Folder')
		CreateToolTip(self.closetabtn, text='Close Tab')
		nf.pack(side='top', fill='x')
		self.tree = ttk.Treeview(frame)
		self.tree.bind("<Double-Button-1>", openthisfile)
		self.nodes = dict()
		ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
		#xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
		self.tree.configure(yscrollcommand=ysb.set)#,xscrollcommand=xsb.set)
		self.tree.heading('#0', text='FOLDERS', anchor='w')
		self.tree.column('#0',width=50,minwidth=100)
		ysb.pack(side=RIGHT,fill=Y)
		#xsb.pack(side=BOTTOM,fill=X)
		self.tree.pack(fill=BOTH,expand=1)
		frame.pack(fill=BOTH,expand=1)
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


filepath = ""

def identify(extension):
	for y in highlight.keys():
		for z in highlight[y]:
			if extension == z:
				return y

try:
	configs = open("./DATA/runner.confscript","r+")
except FileNotFoundError:
	configs = open("./DATA/runner.confscript", "x")

datafile = open("./DATA/runner.confscript").read()
if datafile.isspace():
	isConf = False
else:
	isConf = True

def runnerConf(thisType):
	cmds = cfsread(datafile)
	command = cmds[thisType]['command']
	command = command.replace("$file",'"'+filepath+'"')
	base = filepath.split("/")[-1]
	base = base[:base.find(".")]
	command = command.replace("$base",base.replace(" ","_"))
	command = command.replace("$dir",'"'+"/".join(filepath.split("/")[:-1])+'"')
	log('started {} via {}'.format(filepath,thisType),call='RUNNER')
	subprocess.call("start cmd /k {}".format(command), shell = True)

def getConfs():
	confs = []
	cmds = cfsread(datafile)
	for i in cmds.keys():
		confs.append(i)
	return confs

colors = []
extension = {}

def current_note(*args):
	variable = notebook.select()
	if str(notebook.select()).replace('.!panedwindow.!panedwindow.!panedwindow.!notebook.!frame','') == "":
		variable = 0
	else:
		variable = int(str(notebook.select()).replace('.!panedwindow.!panedwindow.!panedwindow.!notebook.!frame',''))
		if variable == 0:
			pass
		else:
			variable = int(variable) -1
	return variable

class AutocompleteEntry(ttk.Entry):
	"""
	Subclass of tkinter.Entry that features autocompletion.
	To enable autocompletion use set_completion_list(list) to define
	a list of possible strings to hit.
	To cycle through hits use down and up arrow keys.
	"""

	def set_completion_list(self, completion_list):
		self._completion_list = completion_list
		self._hits = []
		self._hit_index = 0
		self.position = 0
		self.bind('<KeyRelease>', self.handle_keyrelease)

	def autocomplete(self, delta=0):
		"""autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
		if delta: # need to delete selection otherwise we would fix the current position
			self.delete(self.position, tkinter.END)
		else: # set position to end so selection starts where textentry ended
			self.position = len(self.get())
		# collect hits
		_hits = []
		for element in self._completion_list:
			if element.startswith(self.get().lower()):
				_hits.append(element)
		# if we have a new hit list, keep this in mind
		if _hits != self._hits:
			self._hit_index = 0
			self._hits=_hits
		# only allow cycling if we are in a known hit list
		if _hits == self._hits and self._hits:
			self._hit_index = (self._hit_index + delta) % len(self._hits)
		# now finally perform the auto completion
		if self._hits:
			self.delete(0,tkinter.END)
			self.insert(0,self._hits[self._hit_index])
			self.select_range(self.position,tkinter.END)

	def handle_keyrelease(self, event):
		"""event handler for the keyrelease event on this widget"""
		if event.keysym == "BackSpace":
			self.delete(self.index(tkinter.INSERT), tkinter.END)
			self.position = self.index(tkinter.END)
		if event.keysym == "Left":
			if self.position < self.index(tkinter.END): # delete the selection
				self.delete(self.position, tkinter.END)
			else:
				self.position = self.position-1 # delete one character
				self.delete(self.position, tkinter.END)
		if event.keysym == "Right":
			self.position = self.index(tkinter.END) # go to end (no selection)
		if event.keysym == "Down":
			self.autocomplete(1) # cycle to next hit
		if event.keysym == "Up":
			self.autocomplete(-1) # cycle to previous hit
		# perform normal autocomplete if event is a single key or an umlaut
		if len(event.keysym) == 1:# or event.keysym in tkinter_umlauts:
			self.autocomplete()

class CustomText(Text):
	def __init__(self, *args, **kwargs):
		"""A text widget that report on internal widget commands"""
		Text.__init__(self, *args, **kwargs)

		# create a proxy for the underlying widget
		self._orig = self._w + "_orig"
		self.tk.call("rename", self._w, self._orig)
		self.tk.createcommand(self._w, self._proxy)

	def _proxy(self, command, *args):
		cmd = (self._orig, command) + args
		result = self.tk.call(cmd)
		if command in ("insert", "delete", "replace"):
			self.event_generate("<<TextModified>>")
		return result

def newrunner():
	global configs
	configs = open("./DATA/runner.confscript","r+")
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
		log('created {}'.format(name.get()),call='RUNNER')
	def switchFunction():
		if gui.get():
			switch.config(text='Console')
		#else:
			#switch.config(text='No Console')
	def helpwindow():
		a = tk.Toplevel(root)
		a.wm_attributes("-topmost",1)
		a.resizable(False,False)
		a.iconbitmap(r"./DATA/icons/favicon.v3.ico")
		a.title("Help")
		b = Label(a,text = 'Keywords',font="Consolas", anchor='w').pack(expand=True)
		b = Label(a,text = '$file: filepath',font="Consolas", anchor='w').pack(expand=True)
		b = Label(a,text = '$base: file base name',font="Consolas", anchor='w').pack(expand=True)
		b = Label(a,text = '$dir: file directory',font="Consolas", anchor='w').pack(expand=True)
		b = Label(a,text = '\nNOTE: only click "Confirm" & close\nnew runner popup to avoid errors',font="Consolas 12 \ bold", anchor='w').pack(expand=True)
		a.mainloop()
	conf = tk.Toplevel(root)
	conf.wm_attributes("-topmost",1)
	conf.iconbitmap(r"./DATA/icons/favicon.v3.ico")
	conf.resizable(False, False)
	conf.title("Configure new Runner")
	conf.geometry("400x250")
	gui = BooleanVar()
	label = Label(conf,text = "Runner Name", font = "consolas")
	name = ttk.Entry(conf,width = 25, font = "consolas")
	name.place(x = 150, y = 10)
	label.place(x=10,y=16)
	label = Label(conf,text = "Command", font = "consolas")
	label.place(x=10,y=55)
	entry = AutocompleteEntry(conf,width = 25, font = "consolas")
	entry.set_completion_list((u'$file', u'$base', u'$dir', u'/k'))
	entry.place(x=150, y=50)
	entry.insert(0, 'compiler -o $base $file')
	label = Label(conf, text='Extensions',font='consolas')
	label.place(x=10,y=100)
	entriee = ttk.Entry(conf,width=25, font='Consolas')
	entriee.place(x=150,y=95)
	entriee.insert(0, '.py,.cpp,.h')
	helptxt = Label(conf,text = "Do you need some", font = "consolas")
	helptxt.place(x=60,y=150)
	helpbtn = ttk.Button(conf,text = "Help",command = lambda:helpwindow())
	helpbtn.place(x=220,y=150)
	submit = ttk.Button(conf,text = "Confirm", command = lambda:done())
	submit.place(x=125,y=200)
	conf.mainloop()

def runconf(*args):
	evaled = cfsread(datafile)
	for i in evaled.keys():
		for x in evaled[i]['extensions']:
			if extension[current_note()] in x:
				thisext = i
	try:
		runnerConf(thisext)
	except:
		pass

thisroot = tk.Tk()
log('Main Window created')
thisroot.iconbitmap(r"./data/icons/favicon.v3.ico")
log('icon added')
thisroot.title(configuration['Looks']['WindowTitle'])
log('title set')
windowWidth = 800
windowHeight = 550
screenWidth  = thisroot.winfo_screenwidth()
screenHeight = thisroot.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
thisroot.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))
log('geometry set')
style = ttk.Style(thisroot)

statusbar = tk.Frame(thisroot)
statusbar.pack(side='bottom', anchor='s', fill='x')

status = Label(statusbar, text = 'setting up!', anchor='w')
status.pack(side='left')

cursyntax = StringVar()
languages = [data.config['Looks']['InitialSyntax']]
for i in highlight.keys():
	languages.append(i)
syntaxchoose = ttk.OptionMenu(statusbar, cursyntax, *languages,command=lambda name="__main__": note[current_note()].config(language=cursyntax.get()))
syntaxchoose.pack(side='right')

rootframe = tk.PanedWindow(thisroot,handlesize=5,orient=tk.VERTICAL)
rootframe.pack(side='right',expand=True,fill='both')
splitter = tk.PanedWindow(rootframe, handlesize=5, orient=tk.HORIZONTAL)

filespaneframe = tk.Frame(splitter)
lookspaneframe = tk.Frame(splitter)
settipaneframe = tk.Frame(splitter)

toolbar = ttk.Frame(thisroot)
toolbar.pack(fill='both',expand=True)
toolbar_menu_icon = PhotoImage(file = "./DATA/icons/logo-mini.png", master = toolbar).subsample(5)
toolbar_menu = ttk.Button(toolbar,image=toolbar_menu_icon, command=about)
toolbar_menu.pack(fill='x')
tools_files_icon = PhotoImage(file = "./DATA/icons/{}/sidebar.files.png".format(data.config['Looks']['Icons']['Theme']), master = toolbar)
tools_files = ttk.Button(toolbar,image=tools_files_icon, command=togglesidepane)
tools_files.pack(fill='x')
tools_runner_icon = PhotoImage(file = "./DATA/icons/{}/sidebar.runner.png".format(data.config['Looks']['Icons']['Theme']), master = toolbar)
tools_runner = ttk.Button(toolbar,image=tools_runner_icon, command=togglerunner)
tools_runner.pack(fill='x')
tools_looks_icon = PhotoImage(file = "./DATA/icons/{}/sidebar.looks.png".format(data.config['Looks']['Icons']['Theme']), master = toolbar)
tools_looks = ttk.Button(toolbar,image=tools_looks_icon, command=togglelookpane)
tools_looks.pack(fill='x')
tools_settings_icon = PhotoImage(file = "./DATA/icons/{}/sidebar.settings.png".format(data.config['Looks']['Icons']['Theme']), master = toolbar)
tools_settings = ttk.Button(toolbar,image=tools_settings_icon, command=togglesetti)
tools_settings.pack(side='bottom',anchor='s',fill='x')

log('Icons made and added',call='SIDEBAR')

projectBar_icon_newfile = PhotoImage(file='./DATA/icons/{}/project.newfile.png'.format(data.config['Looks']['Icons']['Theme']), master = toolbar)
projectBar_icon_newfold = PhotoImage(file='./DATA/icons/{}/project.newfolder.png'.format(data.config['Looks']['Icons']['Theme']), master = toolbar)
projectBar_icon_closefi = PhotoImage(file='./DATA/icons/{}/project.closefile.png'.format(data.config['Looks']['Icons']['Theme']))

img100x100 = tk.PhotoImage(data=zlib.decompress(data.logo))

newtabICON = PhotoImage(file='./DATA/icons/{}/main.newtab.png'.format(data.config['Looks']['Icons']['Theme']))

root = tk.PanedWindow(splitter,orient=VERTICAL,handlesize=5)

runnerpaneframe = tk.Frame(splitter)
framed = PathView(filespaneframe, paths=[])
settingpane= Settings(settipaneframe)
lookpane = lookspane(lookspaneframe)
runpane= runnerpane(runnerpaneframe)

splitter.add(root)

def termreset():
	global tkterminal
	tkterminal.pack_forget()
	tkterminal = Terminal(termframe, font='Consolas 10')
	tkterminal.basename = "$"
	tkterminal.shell = True
	tkterminal.pack(side='left',anchor='w',fill='both',expand=True)
	log('reset',call='TERMINAL')

from tkterminal import *
termframe = ttk.Frame()
termicon_clear = PhotoImage(file= './DATA/icons/{}/terminal.clear.png'.format(data.config['Looks']['Icons']['Theme']))
termicon_reset = PhotoImage(file= './DATA/icons/{}/terminal.restart.png'.format(data.config['Looks']['Icons']['Theme']))
tkterminal = Terminal(termframe, font='Consolas 10', relief='flat')
tkterminal.basename = "$"
tkterminal.shell = True
newframe = tk.Frame(termframe)
newframe.pack(side='right',anchor='ne')
tkterm_clear = tk.Button(newframe,anchor='n',image=termicon_clear, relief='flat', borderwidth=0,command=lambda:tkterminal.clear())
tkterm_reset = tk.Button(newframe,anchor='n',image=termicon_reset, relief='flat', borderwidth=0,command=lambda:termreset())
CreateToolTip(tkterm_clear, "Clear the terminal")
CreateToolTip(tkterm_reset, "Restart the terminal\nJust in case you crashed..")
tkterm_clear.pack(side='top')
tkterm_reset.pack(side='top')
tkterminal.pack(side='left',anchor='w',fill='both',expand=True)
log('placed',call='TERMINAL')
termframe.pack(fill='both',expand=True)
rootframe.add(splitter,height=450)
root.add(termframe,height=200)

try:
	themefolder = configuration['Looks']['Theme']['Folder']
	listdir = os.listdir(themefolder)
	themeslist = []
	for i in listdir:
		if i.lower().endswith('.whtheme'):
			themeslist.append(i)
	default_theme = configuration['Looks']['Theme']['Default']
	if default_theme != '__default__':
		zipfile.ZipFile(themefolder+'/'+default_theme,'r').extractall(tempfile.gettempdir()+"/WhirlEdit/")
		themefile = tempfile.gettempdir()+"/WhirlEdit/"+read(open(tempfile.gettempdir()+"/WhirlEdit/__init__.whirldata").read())['main'][0]
		themebase = read(open(tempfile.gettempdir()+"/WhirlEdit/__init__.whirldata").read())['name'][0]
		thisroot.tk.call('source', themefile)
		style.theme_use(themebase)
		log('set theme {}'.format(themebase),call='LOOKS')
	else:
		pass
	default_highlight = configuration['Looks']['Scheme']['Folder']+configuration['Looks']['Scheme']['Default']+'.json'
	log('set scheme {}'.format(default_highlight),call='LOOKS')
except Exception as e:
	log('({}) {}'.format(type(e).__name__, e), call='ERROR')
	messagebox.showerror(type(e).__name__, e)
	sys.exit()

note        = {}
openedfiles = {}
canvas      = {}
scrolly     = {}
scrollx     = {}
var         = 0

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
		variable = 0
	else:
		variable = int(str(notebook.select()).replace('.!panedwindow.!panedwindow.!panedwindow.!notebook.!frame',''))
		if variable == 0:
			pass
		else:
			variable = int(variable) -1
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
		thisroot.quit()

def saveAsFile(*args):
	global notebook
	global extension
	global filepath
	filepath = asksaveasfilename(defaultextension="",filetypes=[ ("All Files", "*.*"),("Text Files", "*.txt"),("Ada"         ,[".adb",".ads"]),("Bash"        ,[".sh",".csh",".ksh"]),("Batch"       ,[".cmd",".bat"]),("BrainFuck"   ,[".b",".bf"]),("C"           ,[".c",".h"]),("CMake"       ,[]),("CoffeeScript",[".coffee",".cson",".litcoffee"]),("CSS"         ,[".css"]),("C#"          ,[".cs",".csx"]),("C++"         ,[".cc",".cpp",".cxx",".c++",".hh",".hpp",".hxx",".h++"]),("Dart"        ,[".dart"]),("Delphi"      ,[".dpr"]),("Dockerfile"  ,[".dockerfile"]),("Fortran"     ,[".f",".f90",".f95"]),("Go"          ,[".go"]),("Groovy"      ,[".groovy",".gvy",".gradle",".jenkinsfile"]),("Haskell"     ,[".hs",".lhs"]),("HTML"        ,[".htm",".html"]),("Java"        ,[".java",".jar",".class"]),("JavaScript"  ,[".js",".cjs",".mjs"]),("JSON"        ,[".json"]),("Kotlin"      ,[".kt",".kts",".ktm"]),("Lisp"        ,[".lsp"]),("Lua"         ,[".lua"]),("MATLAB"      ,[".m",".p",".mex",".mat",".fig",".mlx",".mlapp",".mltbx"]),("MakeFile"    ,[".make",".makefile"]),("NASM"        ,[".asm",".asm",".inc"]),("Objective-C" ,[".mm"]),("Perl"        ,[".plx",".pl",".pm",".xs",".t",".pod"]),("PHP"         ,[".php",".phar",".phtml",".pht",".phps"]),("Powershell"  ,[".ps1"]),("Python"      ,[".py",".pyi",".pyc",".pyd",".pyo",".pyw",".pyz"]),("R"           ,[".r",".rdata",".rds",".rda"]),("Ruby"        ,[".rb"]),("Swift"       ,[".swift"]),("SQL"         ,[".sql"]),("Tcl"         ,[".tcl",".tbc"]),("TypeScript"  ,[".ts",".tsx"]),("Vim"         ,[".vim"]),("YAML"        ,[".yaml",".yml"]),])
	if not filepath:
		return
	with open(filepath, "w") as output_file:
		extension[current_note()] = "."+filepath.split(".")[-1]
		tabfmt[current_note()] = "."+filepath.split(".")[-1]
		variable = int(current_note())
		text = note[variable].get(1.0, tk.END)
		output_file.write(text)
		log('saved file {}'.format(filepath), call='FILES')
	notebook.tab(frames[int(current_note())], text = filepath.split("/")[-1]+"   ")
	note[current_note()].config(language=identify(filepath.split("/")[-1])+"   ")
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
			extension[current_note()],tabfmt[current_note()] = "."+openedfiles[variable].split(".")[-1]
			text = note[variable].get(1.0, tk.END)
			output_file.write(text)
			notebook.tab(frames[variable], text = openedfiles[current_note()].split("/")[-1]+"   ")
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
		extension[current_note()] = "."+filepath.split(".")[-1]
		tabfmt[current_note()]= "."+filepath.split(".")[-1]
		note[variable].delete(1.0,END)
		file = open(filepath,"r")
		note[current_note()]["language"] = identify(filepath.split("/")[-1])
		note[variable].insert(1.0,file.read()[:-1])
		openedfiles[variable] = filepath
		file.close()
		notebook.tab(frames[variable], text = filepath.split("/")[-1]+"   ")
		note[current_note()].config(language=identify("."+filepath.split(".")[-1]))
		log('opened file {}'.format(filepath), call='FILES')

def select_all(event):
	note[current_note()].tag_add(SEL, "1.0", END)
	note[current_note()].mark_set(INSERT, "1.0")
	note[current_note()].see(INSERT)

frames = {}

def newTab(*args):
	global var
	global notebook
	frames[var] = ttk.Frame(notebook)
	note[var] = (CodeEditor(frames[var],blockcursor=configuration['Looks']['Font']['BlockCursor'],width=40, height=100, language=configuration['Looks']['InitialSyntax'],autofocus=True, insertofftime=0, padx=0, pady=0, font =data.font, highlighter = default_highlight))
	note[var].pack(fill="both", expand=True)
	font = tkfont.Font(font=note[var]['font'])
	note[var].config(tabs=font.measure('    '))
	openedfiles[var] = ""
	notebook.add(frames[var], text='Untitled   ')
	extension[current_note()] = ".*"
	note[var].bind('<Control-Tab>',nexttab)
	note[var].bind("Control-a",select_all)
	var = var + 1
	nexttab()
	tabfmt[current_note()] = '.py'
	log('new tab added', call='TABS')

Menubar = Menu(root, activebackground ="#0084FF", activeforeground = "#FFFFFF",bg = "#FFFFFF", fg = "#0084FF" ,font = "consolas")

Filemenu = Menu(root, tearoff = 0)
Filemenu.add_command(label="New",command=newTab)
Filemenu.add_separator()
Filemenu.add_command(label="Open", command=openFile)
Filemenu.add_command(label="Save", command=saveFile)
Filemenu.add_command(label="Save As", command=saveAsFile)
Filemenu.add_separator()
Filemenu.add_command(label="Close", command=deltab)
Filemenu.add_separator()
Filemenu.add_command(label="Exit", command=thisroot.destroy)
Menubar.add_cascade(label="File", menu=Filemenu)

viewMenu = Menu(root,tearoff=0)
viewMenu.add_command(label = "Toggle Project Pane", command = lambda:togglesidepane())
viewMenu.add_command(label = "Toggle Fullscreen", command = lambda:fullscreen())
Menubar.add_cascade(label = "View", menu = viewMenu)

toolsMenu = Menu(root,tearoff=0)
confmenu = Menu(root,tearoff=0)
runmenu = Menu(root,tearoff = 0)

runner_command = StringVar()
if isConf:
	for i in getConfs():
		if i != "@":
			runmenu.add("command",label = i, command = lambda i=i: runnerConf(i))
	runmenu.add_separator()
runmenu.add_command(label= "New Runner",command = lambda:newrunner())
toolsMenu.add_cascade(label = "Runner", menu = runmenu)
toolsMenu.add_command(label = "Open cmd here", command = lambda:opencmd())
Menubar.add_cascade(label="Tools",menu = toolsMenu)

syntaxMenu = Menu(root,tearoff=0)
setSyntaxMenu = Menu(root,tearoff=0)
for i in highlight.keys():
	setSyntaxMenu.add_command(label = i,command = lambda lang=i: set_syntax(lang))
syntaxMenu.add_cascade(label = "Syntax", menu = setSyntaxMenu)
Menubar.add_cascade(label = "Looks",menu = syntaxMenu)

Helpmenu = Menu(root, tearoff = 0)
Helpmenu.add_command(label = "Website", command=lambda:webbrowser.open("http://Whirlpool-Programmer.github.io/software/WhirlEdit/"))
Helpmenu.add_separator()
Helpmenu.add_command(label = "Changelog", command=None)
Helpmenu.add_command(label = "About",command = about)
Menubar.add_cascade(label = "Help", menu=Helpmenu)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

newtabbtn=tk.Button(thisroot,relief='flat', borderwidth=0,image=newtabICON, command=newTab)
newtabbtn.place(anchor='ne',relx = 1, x =-5, y = 5)

notebook = Notebook(root)
notebook.grid(sticky = N + E + S + W)
notebook.bind("<B1-Motion>", reorder)
def nexttab(*args):
	try:
		notebook.select(current_note()+1)
	except:
		notebook.select(0)

newTab()

extension[current_note()] = ".*"

btn = ttk.Button(thisroot,text = 'NEW')
btn.place(anchor='ne')

if len(sys.argv) >= 2:
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

root.add(notebook,before=termframe,height=450)
class generate:
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
	tkTextmenu.entryconfigure("Cut",command=lambda: generate.cut(_widget))
	tkTextmenu.entryconfigure("Copy",command=lambda: generate.copy(_widget))
	tkTextmenu.entryconfigure("Paste",command=lambda: generate.paste(_widget))
	tkTextmenu.tk.call("tk_popup", tkTextmenu, event.x_root, event.y_root)

def startfind(*args):
	txtutils.Find(thisroot, note[current_note()])

def startreplace(*args):
	txtutils.Replace(thisroot, note[current_note()])

tkTextmenu = tk.Menu(root, tearoff=0)
tkTextmenu.add_command(label="Cut")
tkTextmenu.add_command(label="Copy")
tkTextmenu.add_command(label="Paste")

notebook.bind("<Double-Button>", newTab)
thisroot.bind_all(configuration['Key Bindings']['Save'], saveFile)
thisroot.bind_all(configuration['Key Bindings']['New'], newTab)
thisroot.bind_all(configuration['Key Bindings']['Close'], deltab)
thisroot.bind_all(configuration['Key Bindings']['Open'], openFile)
thisroot.bind_all("<Control-F5>",runfile)
thisroot.bind_all(configuration['Key Bindings']['Run'],runconf)
thisroot.bind_all(configuration['Key Bindings']['Open cmd'], opencmd)
thisroot.bind_all("<Key>",update)
thisroot.bind_all("<Button-1>",update)
thisroot.bind_all('<Control-Tab>',nexttab)
notebook.bind_all('<Control-Tab>',nexttab)
thisroot.bind_all(configuration['Key Bindings']['Fullscreen'],fullscreen)
thisroot.bind_class("Text", "<Button-3><ButtonRelease-3>", texteditmenu)
thisroot.bind('<Control-f>',startfind)
thisroot.bind('<Control-h>',startreplace)
thisroot.config(menu = None)
thisroot.after(1000, exec('datafile = open("./DATA/runner.confscript").read()'))
thisroot.after(100, update)
log('binded all keystrokes')
log('starting main window')

try:
	thisroot.mainloop()
except Exception as e:
	log('({}) {}'.format(type(e).__name__, e), call='ERROR')
	messagebox.showerror(type(e).__name__, e)

configs.close()
open('./DATA/configure.yaml','w+').write(yaml.dump(data.config))
try:
	shutil.rmtree(tempfile.gettempdir()+'/WhirlEdit')
	log('removed TEMP/WhirlEdit folder')
except:
	pass

log('removed logs file')

log('Exiting program')
print('** See you later **')