import os
import yaml
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkfont
from tkinter.filedialog import askopenfilename, asksaveasfilename
import subprocess
import shutil
import tkinter
import zipfile
import tempfile
from wday import *
from tkcode import CodeEditor
import webbrowser
import re

from pygments.lexer import RegexLexer
from pygments.token import Comment, Name, String, Number, Punctuation

class WhirlDataLexer(RegexLexer):

    name = 'WhirlData'
    aliases = ['whirldata']
    filenames = ['*.whirldata',"*.wday","*.whdata"]

    tokens = {
        'root': [
            (r'~.*$', Comment.Single),
            (r'@.*$', Name.Other),
            (r'\'\$.*\'', Name.Variable),
            (r'\d(?:_?\d)*', Number.Integer),
            (r'::', Punctuation),
            (r'\'.*\'', String.Single),
        ],
    }

class defaults:
	configuration = """
Looks:
  Theme:
    Default: azure-dark.whTheme
    Folder: ./Themes/
  Scheme:
    Default: azure.json
    Folder: ./Schemes/
  Font:
    Font: Consolas
    Size: 12

Key Bindings:
  File:
    Save: <Control-s>
    New: <Control-s>
    Close: <Control-s>
    Open: <Control-o>
  View:
    Fullscreen: <F11>
    Project: <Control-Shift-P>
  Runner:
    Run: <F5>
    Terminal: <Control-Shift-T>

	"""

try:
	configuration = (yaml.safe_load(open('configure.yaml').read()))
except:
	configuration = (yaml.safe_load(defaults.configuration))
openedfolders = []

highlight = {
			"WhirlData"   : ['*.whirldata',"*.wday","*.whdata"],
			"Ada"         : [".adb",".ads"],
			"Bash"        : [".sh",".csh",".ksh"],#new
			"Batch"       : [".cmd",".bat"],#new
			"BrainFuck"   : [".b",".bf"],
			"C"           : [".c",".h"],
			"CMake"       : [],#new
			"CoffeeScript": [".coffee",".cson",".litcoffee"],#new
			"CSS"         : [".css"],
			"C#"          : [".cs",".csx"],
			"C++"         : [".cc",".cpp",".cxx",".c++",".hh",".hpp",".hxx",".h++"],
			"Dart"        : [".dart"],
			"Delphi"      : [".dpr"],
			"Dockerfile"  : [".dockerfile"],#new
			"Fortran"     : [".f",".f90",".f95"],#new
			"Go"          : [".go"],
			"Groovy"      : [".groovy",".gvy",".gradle",".jenkinsfile"],#new
			"Haskell"     : [".hs",".lhs"],
			"HTML"        : [".htm",".html"],
			"Java"        : [".java",".jar",".class"],
			"JavaScript"  : [".js",".cjs",".mjs"],
			"JSON"        : [".json"],#new
			"Kotlin"      : [".kt",".kts",".ktm"],
			"Lisp"        : [".lsp"],
			"Lua"         : [".lua"],
			"MATLAB"      : [".m",".p",".mex",".mat",".fig",".mlx",".mlapp",".mltbx"],
			"MakeFile"    : [".make",".makefile"],#new
			"NASM"        : [".asm",".asm",".inc"],#new
			"Objective-C" : [".mm"],
			"Perl"        : [".plx",".pl",".pm",".xs",".t",".pod"],
			"PHP"         : [".php",".phar",".phtml",".pht",".phps"],
			"Powershell"  : [".ps1"],#new
			"Python"      : [".py",".pyi",".pyc",".pyd",".pyo",".pyw",".pyz"],
			"R"           : [".r",".rdata",".rds",".rda"],
			"Ruby"        : [".rb"],
			"Swift"       : [".swift"],
			"SQL"         : [".sql"],
			"Tcl"         : [".tcl",".tbc"],
			"TypeScript"  : [".ts",".tsx"],
			"Vim"         : [".vim"],#new
			"YAML"        : [".yaml",".yml"],#new
			}

nothing = [1,0,1]

def about(*args):
	a = tk.Toplevel(thisroot)
	a.wm_attributes("-topmost",1)
	a.title('About Whirledit')
	a.resizable(False,False)
	a.iconbitmap(r"favicon.v3.ico")
	a.geometry("300x200")
	b = Label(a,text='WhirlEdit Insiders',font='Consolas 20')
	b.pack()
	c = Label(a,text='v3.0.500',font='Consolas 10')
	c.pack()
	d = Label(a,text='\nWritten in python\nby Whirlpool-Programmer\n',font='Consolas 15')
	d.pack()
	e = ttk.Button(a,text='GitHub', command=lambda:webbrowser.open('http://Whirlpool-Programmer.github.io/software/WhirlEdit'))
	e.pack()

def fullscreen(*args):
	if nothing[1] == 0:
		thisroot.wm_attributes("-fullscreen",1)
		nothing[1] = 1
	else:
		thisroot.wm_attributes("-fullscreen",0)
		nothing[1] = 0

def set_syntax(lang):
	note[curnote2()].config(language=lang)

def togglesidepane(*args):
	global nothing
	if nothing[0] == 0:
		splitter.forget(filespaneframe)
		nothing[0] = 1
	else:
		splitter.add(filespaneframe, before = root,width=200)
		splitter.forget(lookspaneframe)
		nothing[0] = 0

def togglelookpane(*args):
	global nothing
	if nothing[2] ==0:
		splitter.forget(lookspaneframe)
		nothing[2] = 1
	else:
		splitter.add(lookspaneframe, before = root,width=200)
		splitter.forget(filespaneframe)
		nothing[2] =0

def update(*args):
	fdir = "/".join(openedfiles[curnote2()].split("/")[:-1])
	line = note[curnote2()].index(tk.INSERT).split('.')
	status['text'] = "Line {}, Column {}".format(line[0],line[1])
	if fdir in openedfolders:
		pass
	else:
		framed.add(fdir)
		openedfolders.append(fdir)

def openthisfile(event):
	global extension
	global filepath
	item_id = event.widget.focus()
	item = event.widget.item(item_id)
	values = item['text']
	print(values)
	if os.path.isfile(values):
		variable = curnote2()
		filepath = values
		extension[curnote()] = "."+filepath.split(".")[-1]
		note[variable].delete(1.0,END) 
		file = open(filepath,"r") 
		note[curnote2()]["language"] = identify(filepath.split("/")[-1])
		note[variable].insert(1.0,file.read()) 
		openedfiles[variable] = filepath
		file.close() 
		notebook.tab(frames[variable], text = filepath.split("/")[-1])
		note[curnote2()].config(language=identify("."+filepath.split(".")[-1]))

class lookspane(object):
	def __init__(self,master):
		frame = tk.Frame(master)
		curscheme = tk.StringVar()
		curscheme_values = ['Scheme']
		for i in os.listdir(configuration['Looks']['Scheme']['Folder']):
			if i.lower().endswith('.json'):
				curscheme_values.append(i[:-5])
		self.b = ttk.OptionMenu(frame, curscheme, *curscheme_values, command = lambda a='s':note[curnote2()].config(highlighter = configuration['Looks']['Scheme']['Folder']+curscheme.get()+'.json'))
		self.d = tk.Label(frame,text='Syntax')
		self.d.grid(row=2,column=0)
		self.e = tk.Label(frame,text='Scheme')
		self.e.grid(row=3,column=0)
		cursyntax = StringVar()
		languages = ['Choose']
		for i in highlight.keys():
			languages.append(i)
		self.c = ttk.OptionMenu(frame, cursyntax, *languages,command=lambda name="__main__": note[curnote2()].config(language=cursyntax.get()))
		self.c.grid(row=2,column=1)
		self.b.grid(row=3,column=1,sticky ="SE")
		frame.grid(sticky='NSEW')

class PathView(object):
	def add(self,path):
		abspath = os.path.abspath(path)
		self.insert_node('', abspath.split('\\')[-1], abspath)
		self.tree.bind('<<TreeviewOpen>>', self.open_node)
	def __init__(self, master, paths):
		frame = tk.Frame(master)
		self.tree = ttk.Treeview(frame)
		self.tree.bind("<Double-Button-1>", openthisfile)
		self.nodes = dict()
		ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
		self.tree.configure(yscroll=ysb.set)
		self.tree.heading('#0', text='FOLDERS', anchor='w')
		ysb.pack(side=RIGHT,fill=Y)
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
	configs = open("runner.whirldata","r+")
except FileNotFoundError:
	configs = open("runner.whirldata", "x")

datafile = open("runner.whirldata").read()
if datafile.isspace():
	isConf = False
else:
	isConf = True

def runnerConf(thisType):
	print(thisType)
	cmds = read(datafile)
	command = cmds[thisType][1]
	command = command.replace("$file",'"'+filepath+'"')
	base = filepath.split("/")[-1]
	base = base[:base.find(".")]
	command = command.replace("$base",base.replace(" ","_"))
	command = command.replace("$dir",'"'+"/".join(filepath.split("/")[:-1])+'"')
	subprocess.call("start cmd /k {}".format(command), shell = True)

def getConfs():
	confs = []
	cmds = read(datafile)
	for i in cmds.keys():
		confs.append(i)
	return confs

colors = []
extension = {}

def curnote2(*args):
	variable = notebook.select()
	if notebook.select().replace('.!panedwindow.!frame3.!notebook.!frame','') == "":
		variable = 0
	else:
		variable = int(notebook.select().replace('.!panedwindow.!frame3.!notebook.!frame',''))
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
	global conf
	def done():
		print(entry.get())
		thisconf = ""
		configs.writelines(datafile+'\n{}::[["{}"]::"{}"]'.format(name.get(),extension[curnote()],entry.get()))
		print(thisconf)
		conf.quit()
	def switchFunction():
		if gui.get():
			switch.config(text='Console')
		#else:
			#switch.config(text='No Console')
	def helpwindow():
		a = tk.Toplevel(conf)
		a.wm_attributes("-topmost",1)
		a.resizable(False,False)
		a.iconbitmap(r"favicon.v3.ico")
		a.title("Help")
		helpvartxt = """
Keywords:                               
  $file                                 
	the file path.                      
  $base                                 
	the base name of the file.          
  $dir                                  
	the folder where file is located.   
		"""
		b = Label(a,text = helpvartxt,font="Consolas")
		b.pack(side = LEFT)
		a.mainloop()
	conf = tk.Toplevel(root)
	conf.wm_attributes("-topmost",1)
	conf.iconbitmap(r"favicon.v3.ico")
	conf.resizable(False, False)
	conf.title("Configure runner for {} files".format(extension[curnote()]))
	conf.geometry("400x200")
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
	helptxt = Label(conf,text = "Do you need some", font = "consolas")
	helptxt.place(x=60,y=100)
	helpbtn = ttk.Button(conf,text = "Help",command = lambda:helpwindow())
	helpbtn.place(x=220,y=100)
	submit = ttk.Button(conf,text = "Confirm & Create Runner", command = lambda:done())
	submit.place(x=125,y=150)
	conf.mainloop()

def runconf(*args):
	evaled = read(datafile)
	for i in evaled.keys():
		if i=="@":
			pass
		else:
			for x in evaled[i][0]:
				if x == extension[curnote2()]:
					thisext = i
	try:
		runnerConf(thisext)
	except:
		pass
	
thisroot = tk.Tk()
thisroot.iconbitmap(r"favicon.v3.ico")
thisroot.title('WhirlEdit')
windowWidth = 800
windowHeight = 530
screenWidth  = thisroot.winfo_screenwidth()
screenHeight = thisroot.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
thisroot.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))
style = ttk.Style(thisroot)

splitter = tk.PanedWindow(thisroot, handlesize=2, orient=tk.HORIZONTAL)
splitter.pack(side='right',expand=True, fill='both')

filespaneframe = tk.Frame(splitter, bg='#202020')
lookspaneframe = tk.Frame(splitter,bg='#202020')
root = tk.Frame(splitter)
framed = PathView(filespaneframe, paths=[])
lookpane = lookspane(lookspaneframe)

toolbar = tk.Frame(thisroot)
toolbar.pack()

toolbar_menu_icon = PhotoImage(file = "./logo.sq.png", master = toolbar).subsample(6)
toolbar_menu = tk.Button(toolbar,image=toolbar_menu_icon, borderwidth=0, command=about)
toolbar_menu.pack()

tools_files_icon = PhotoImage(file = "./icons/wh3.icons-files.png", master = toolbar)
tools_files = tk.Button(toolbar,image=tools_files_icon, borderwidth=0, command=togglesidepane)
tools_files.pack()

tools_project_icon = PhotoImage(file = "./icons/wh3.icons-project.png", master = toolbar)
tools_project = tk.Button(toolbar,image=tools_project_icon, borderwidth=0, command=None)
tools_project.pack()

tools_runner_icon = PhotoImage(file = "./icons/wh3.icons-runner.png", master = toolbar)
tools_runner = tk.Button(toolbar,image=tools_runner_icon, borderwidth=0, command=None)
tools_runner.pack()

tools_settings_icon = PhotoImage(file = "./icons/wh3.icons-settings.png", master = toolbar)
tools_settings = tk.Button(toolbar,image=tools_settings_icon, borderwidth=0, command=None)
tools_settings.pack()

tools_looks_icon = PhotoImage(file = "./icons/wh3.icons-looks.png", master = toolbar)
tools_looks = tk.Button(toolbar,image=tools_looks_icon, borderwidth=0, command=togglelookpane)
tools_looks.pack(side='bottom')

splitter.add(root)
try:
	themefolder = configuration['Looks']['Theme']['Folder']
	listdir = os.listdir(themefolder)
	themeslist = []
	for i in listdir:
		if i.lower().endswith('.whtheme'):
			themeslist.append(i)
	default_theme = configuration['Looks']['Theme']['Default']
	zipfile.ZipFile(themefolder+'/'+default_theme,'r').extractall(tempfile.gettempdir()+"/whTheme/")
	themefile = tempfile.gettempdir()+"/whTheme/"+read(open(tempfile.gettempdir()+"/whTheme/__init__.whirldata").read())['main'][0]
	themebase = read(open(tempfile.gettempdir()+"/whTheme/__init__.whirldata").read())['name'][0]
	thisroot.tk.call('source', themefile)
	style.theme_use(themebase)
	default_highlight = configuration['Looks']['Scheme']['Folder']+configuration['Looks']['Scheme']['Default']
except:
	default_highlight = 'azure'

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
		subprocess.call('start cmd /k cd /d "{}"'.format(cwd), shell=True)
	except:
		subprocess.call('start cmd /k "{}"'.format(openedfiles[curnote2()]), shell=True)

def runfile(*args):
	try:
		cwd = "/".join(filepath.split("/")[:-1])
		drive = cwd[:3]
		subprocess.call('start cmd /k "{}"'.format(openedfiles[curnote2()]), shell=True)
	except:
		subprocess.call('start cmd /k "{}"'.format(openedfiles[curnote2()]), shell=True)

def getpos(*args):
	global pos
	global line
	pos = note[int(curnote())].index("end")
	pos = pos[:-2]
	pos = int(pos)
	pos = pos -1
	print(pos)
	line.set(pos)
def curnote():
	variable = notebook.select()
	if notebook.select().replace('.!panedwindow.!frame3.!notebook.!frame','') == "":
		variable = 0
	else:
		variable = int(notebook.select().replace('.!panedwindow.!frame3.!notebook.!frame',''))
		if variable == 0:
			pass
		else:
			variable = int(variable) -1
	return variable

def deltab(*args):
	try:
		notebook.forget(notebook.select())
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
		extension[curnote()] = "."+filepath.split(".")[-1]
		variable = int(curnote2())
		text = note[variable].get(1.0, tk.END)
		output_file.write(text) 
	notebook.tab(frames[int(curnote2())], text = filepath.split("/")[-1])
	note[curnote2()].config(language=identify(filepath.split("/")[-1]))
	note[curnote2()].update()
	root.update()

def saveFile(*args):
	global notebook
	global extension
	variable = int(curnote2())

	if openedfiles[variable] == "":
		saveAsFile()
	else:
		with open(openedfiles[variable], "w") as output_file:
			extension[curnote()] = "."+openedfiles[variable].split(".")[-1]
			text = note[variable].get(1.0, tk.END)
			output_file.write(text)
			notebook.tab(frames[variable], text = openedfiles[curnote2()].split("/")[-1])

def openFile(*self): 
	#print("a",notebook.select())
	global extension
	global filepath
	if notebook.select() == "":
		newTab()

	variable = curnote2()
	filepath = askopenfilename(defaultextension="*.*", filetypes=[("All Files","*.*"), ("Text","*.txt"),("Ada"         ,[".adb",".ads"]),("Bash"        ,[".sh",".csh",".ksh"]),("Batch"       ,[".cmd",".bat"]),("BrainFuck"   ,[".b",".bf"]),("C"           ,[".c",".h"]),("CMake"       ,[]),("CoffeeScript",[".coffee",".cson",".litcoffee"]),("CSS"         ,[".css"]),("C#"          ,[".cs",".csx"]),("C++"         ,[".cc",".cpp",".cxx",".c++",".hh",".hpp",".hxx",".h++"]),("Dart"        ,[".dart"]),("Delphi"      ,[".dpr"]),("Dockerfile"  ,[".dockerfile"]),("Fortran"     ,[".f",".f90",".f95"]),("Go"          ,[".go"]),("Groovy"      ,[".groovy",".gvy",".gradle",".jenkinsfile"]),("Haskell"     ,[".hs",".lhs"]),("HTML"        ,[".htm",".html"]),("Java"        ,[".java",".jar",".class"]),("JavaScript"  ,[".js",".cjs",".mjs"]),("JSON"        ,[".json"]),("Kotlin"      ,[".kt",".kts",".ktm"]),("Lisp"        ,[".lsp"]),("Lua"         ,[".lua"]),("MATLAB"      ,[".m",".p",".mex",".mat",".fig",".mlx",".mlapp",".mltbx"]),("MakeFile"    ,[".make",".makefile"]),("NASM"        ,[".asm",".asm",".inc"]),("Objective-C" ,[".mm"]),("Perl"        ,[".plx",".pl",".pm",".xs",".t",".pod"]),("PHP"         ,[".php",".phar",".phtml",".pht",".phps"]),("Powershell"  ,[".ps1"]),("Python"      ,[".py",".pyi",".pyc",".pyd",".pyo",".pyw",".pyz"]),("R"           ,[".r",".rdata",".rds",".rda"]),("Ruby"        ,[".rb"]),("Swift"       ,[".swift"]),("SQL"         ,[".sql"]),("Tcl"         ,[".tcl",".tbc"]),("TypeScript"  ,[".ts",".tsx"]),("Vim"         ,[".vim"]),("YAML"        ,[".yaml",".yml"]),]) 
	if filepath == "": 
		filepath = None
	else: 
		extension[curnote()] = "."+filepath.split(".")[-1]
		note[variable].delete(1.0,END) 
		file = open(filepath,"r") 
		note[curnote2()]["language"] = identify(filepath.split("/")[-1])
		note[variable].insert(1.0,file.read()) 
		openedfiles[variable] = filepath
		file.close() 
		notebook.tab(frames[variable], text = filepath.split("/")[-1])
		note[curnote2()].config(language=identify("."+filepath.split(".")[-1]))


def select_all(event):
	note[curnote2()].tag_add(SEL, "1.0", END)
	note[curnote2()].mark_set(INSERT, "1.0")
	note[curnote2()].see(INSERT)

frames = {}

def newTab(*args):
	global var
	global notebook
	frames[var] = ttk.Frame(notebook)
	note[var] = CodeEditor(frames[var],blockcursor=configuration['Looks']['Font']['BlockCursor'],width=40, height=100, language=configuration['Looks']['InitialSyntax'],autofocus=True, insertofftime=0, padx=0, pady=0, font = "{} {}".format(configuration['Looks']['Font']['Font'],configuration['Looks']['Font']['Size']), highlighter = default_highlight)
	note[var].pack(fill="both", expand=True)
	font = tkfont.Font(font=note[var]['font'])
	note[var].config(tabs=font.measure('    '))
	openedfiles[var] = ""
	notebook.add(frames[var], text='Untitled')
	extension[curnote()] = ".*"
	note[var].bind("Control-a",select_all)
	var = var + 1

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
Helpmenu.add_command(label = "About",command = None)
Menubar.add_cascade(label = "Help", menu=Helpmenu)

root.grid_rowconfigure(0, weight=1) 
root.grid_columnconfigure(0, weight=1) 

line = StringVar()
line.set('ready to edit!')

notebook = ttk.Notebook(root)
notebook.grid(sticky = N + E + S + W)
newTab()

status = Label(root, text = line.get(), anchor='w')
status.grid(sticky=E+S+W)
extension[curnote()] = ".*"

notebook.bind("<Double-Button>", newTab)
thisroot.bind(configuration['Key Bindings']['File']['Save'], saveFile)
thisroot.bind(configuration['Key Bindings']['File']['New'], newTab)
thisroot.bind(configuration['Key Bindings']['File']['Close'], deltab)
thisroot.bind(configuration['Key Bindings']['File']['Open'], openFile)
thisroot.bind("<Control-F5>",runfile)
thisroot.bind(configuration['Key Bindings']['Runner']['Run'],runconf)
thisroot.bind(configuration['Key Bindings']['Runner']['Terminal'], opencmd)
thisroot.bind_all("<Key>",update)
thisroot.bind(configuration['Key Bindings']['View']['Fullscreen'],fullscreen)
thisroot.bind(configuration['Key Bindings']['View']['Project'],togglesidepane)
thisroot.config(menu = Menubar)
#try:
thisroot.mainloop()
#except:
	#print("Something's wrong.. :|")
configs.close()
try:
	shutil.rmtree(tempfile.gettempdir()+'/whTheme')
except:
	pass
