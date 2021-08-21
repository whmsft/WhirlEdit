import os
import yaml
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkfont
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesnocancel
import subprocess
import shutil
import tkinter
import zipfile
import tempfile
from wday import read
from tkcode import CodeEditor
import webbrowser

__version__ = 'v3.1-alpha-1'

configuration = """
Looks:
  WindowTitle: WhirlEdit Confetti
  InitialSyntax: python
  Theme:
    Default: sun-valley-dark.whTheme
    Folder: ./DATA/Themes/
  Scheme:
    Default: azure-modified
    Folder: ./DATA/Schemes/
  Font:
    Font: Consolas
    Size: '12'
    BlockCursor: False
  Icons:
    Theme: fluent.dark

Key Bindings:
  Save: <Control-s>
  New: <Control-n>
  Close: <Control-w>
  Open: <Control-o>
  Fullscreen: <F11>
  Project: <Control-Shift-f>
  Run: <F5>
  Terminal: <Control-Shift-t>
"""
try:
	configuration = (yaml.safe_load(open('./DATA/configure.yaml').read()))
except Exception:
	configuration = (yaml.safe_load(configuration))

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
  font = "{} {}".format(configuration['Looks']['Font']['Font'],configuration['Looks']['Font']['Size'])
  isBlockcursor = configuration['Looks']['Font']['BlockCursor']
  config = configuration

def about(*args):
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
		a.geometry("300x200")
		b = Label(a,text='WhirlEdit Insiders',font='Consolas 20')
		b.pack()
		c = Label(a,text=__version__,font='Consolas 10')
		c.pack()
		d = Label(a,text='\nWritten in python\nby Whirlpool-Programmer\n',font='Consolas 15')
		d.pack()
		e = ttk.Button(a,text='GitHub', command=lambda:webbrowser.open('http://Whirlpool-Programmer.github.io/software/WhirlEdit'))
		e.pack()
		tk.Label(a,text=' ').pack()
		a.protocol("WM_DELETE_WINDOW", lambda:nothingmod(4,1))
	else:
		pass

def fullscreen(*args):
	if nothing[1] == 0:
		thisroot.wm_attributes("-fullscreen",1)
		nothing[1] = 1
	else:
		thisroot.wm_attributes("-fullscreen",0)
		nothing[1] = 0

def set_syntax(lang):
	note[curnote2()].config(language=lang)

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

def update(*args):
	thisfile = ""
	if openedfiles[curnote2()] == '' or openedfiles[curnote2()] == ' ':
		thisfile='None'
	else:
		thisfile = openedfiles[curnote2()]
	root.update()
	fdir = "/".join(openedfiles[curnote2()].split("/")[:-1])
	line = note[curnote2()].index(tk.INSERT).split('.')
	note[curnote2()]['font'] = data.font
	note[curnote2()]['blockcursor'] = data.isBlockcursor
	status['text'] = "File: {} | Line {}, Column {}".format(thisfile,line[0],line[1])
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

def changekeybind(*args):
	def getit__(index):
		print(theselabels[i]['text']+"::"+theseentries[i].get())
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

class Settings(object):
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

		frame.pack(expand=True, fill='both')

class runnerpane(object):
	def __init__(self,master):
		frame = tk.Frame(master)
		self.button = ttk.Button(frame,text='Open CMD', command = lambda:opencmd())
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
		self.chooserunner.grid(row=2,column=1, sticky='nsew')
		self.rubbish1 = tk.Label(frame,text=' ')
		self.rubbish1.grid()
		self.button.grid(row=4,column=1)
		self.rubbish2=tk.Label(frame,text=' ').grid()
		self.newrunbtn = ttk.Button(frame,text = 'New Runner',command=lambda:newrunner()).grid(row=6,column=1)
		frame.grid()

class lookspane(object):
	def configsave(self,*args):
		if self.g.get() =='':
			pass
		else:
			thisroot.title(self.g.get())
			data.config['Looks']['WindowTitle'] = thisroot.title()

		if self.i.get() == '':
			pass
		else:
			data.font = self.i.get()
			data.config['Looks']['Font']['Font'] = data.font.split()[0]
			data.config['Looks']['Font']['Size'] = data.font.split()[-1]

		data.isBlockcursor = self.isBlockcursor.get()
		data.config['Looks']['Font']['BlockCursor'] = self.isBlockcursor.get()
		data.config['Looks']['Scheme']['Default'] = self.curscheme.get()

	def __init__(self,master):
		frame = tk.Frame(master)
		self.curscheme = tk.StringVar()
		self.curscheme.set(data.config['Looks']['Scheme']['Default'])
		curscheme_values = [data.config['Looks']['Scheme']['Default']]
		for i in os.listdir(configuration['Looks']['Scheme']['Folder']):
			if i.lower().endswith('.json'):
				curscheme_values.append(i[:-5])
		self.b = ttk.OptionMenu(frame, self.curscheme, *curscheme_values, command = lambda a='s':note[curnote2()].config(highlighter = configuration['Looks']['Scheme']['Folder']+self.curscheme.get()+'.json'))
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
		self.b.grid(row=3,column=1)
		self.f = tk.Label(frame,text='Window Title')
		self.f.grid(row=4,column=0)
		self.g = ttk.Entry(frame,width=20)
		self.g.grid(row=4,column=1)
		self.h = tk.Label(frame,text='Font:')
		self.curfont=StringVar()
		self.curfont.set('{} {}'.format(configuration['Looks']['Font']['Font'],str(configuration['Looks']['Font']['Size'])))
		self.j = tk.Label(frame,text='Font')
		self.j.grid(row=5,column=0)
		self.i = ttk.Entry(frame, text= self.curfont.get())
		self.i.insert(0,self.curfont.get())
		self.i.grid(row=5,column=1)
		self.k = tk.Label(frame,text='Block Cursor')
		self.k.grid(row=6,column=0)
		self.isBlockcursor = BooleanVar()
		self.isBlockcursor.set(data.config['Looks']['Font']['BlockCursor'])
		self.j = ttk.Checkbutton(frame, variable=self.isBlockcursor)
		self.j.grid(row=6, column=1, sticky='w')
		rubbish1 = tk.Label(frame)
		rubbish1.grid()

		self.configconfirm = ttk.Button(frame,text="Save", command=self.configsave)
		self.configconfirm.grid(row=8,column=0)
		frame.grid(sticky='NEWS')


class PathView(object):
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
		self.tree = ttk.Treeview(frame)
		self.tree.bind("<Double-Button-1>", openthisfile)
		self.nodes = dict()
		ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
		self.tree.configure(yscrollcommand=ysb.set,xscrollcommand=xsb.set)
		self.tree.heading('#0', text='FOLDERS', anchor='w')
		self.tree.column('#0',width=50,minwidth=100)
		ysb.pack(side=RIGHT,fill=Y)
		xsb.pack(side=BOTTOM,fill=X)
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
	configs = open("./DATA/runner.whirldata","r+")
except FileNotFoundError:
	configs = open("./DATA/runner.whirldata", "x")

datafile = open("./DATA/runner.whirldata").read()
if datafile.isspace():
	isConf = False
else:
	isConf = True

def runnerConf(thisType):
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
	if notebook.select().replace('.!panedwindow.!panedwindow.!panedwindow.!notebook.!frame','') == "":
		variable = 0
	else:
		variable = int(notebook.select().replace('.!panedwindow.!panedwindow.!panedwindow.!notebook.!frame',''))
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
		configs.write(datafile+'\n{}::[["{}"]::"{}"]'.format(name.get(),'","'.join(entriee.get().split(',')),entry.get()))
		print(thisconf)
		conf.quit()
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
		helpvartxt = """
command entry:
Keywords:
	$file
	the file path.
	$base
	the base name of the file.
	$dir
	the folder where file is located.
"""
		b = Label(a,text = helpvartxt,font="Consolas")
		b.pack(side = 'left',expand=True)
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
	submit = ttk.Button(conf,text = "Confirm & Create Runner", command = lambda:done())
	submit.place(x=125,y=200)
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
thisroot.iconbitmap(r"./data/icons/favicon.v3.ico")
thisroot.title(configuration['Looks']['WindowTitle'])
windowWidth = 800
windowHeight = 550
screenWidth  = thisroot.winfo_screenwidth()
screenHeight = thisroot.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
thisroot.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))
style = ttk.Style(thisroot)

status = Label(thisroot, text = 'Ready to edit | WhirlEdit {}'.format(__version__), anchor='w')
status.pack(side='bottom',anchor='s',fill='x')

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
tools_project_icon = PhotoImage(file = "./DATA/icons/{}/sidebar.edit.png".format(data.config['Looks']['Icons']['Theme']), master = toolbar)
tools_project = ttk.Button(toolbar,image=tools_project_icon, command=None)
tools_project.pack(fill='x')
tools_runner_icon = PhotoImage(file = "./DATA/icons/{}/sidebar.runner.png".format(data.config['Looks']['Icons']['Theme']), master = toolbar)
tools_runner = ttk.Button(toolbar,image=tools_runner_icon, command=togglerunner)
tools_runner.pack(fill='x')
tools_looks_icon = PhotoImage(file = "./DATA/icons/{}/sidebar.looks.png".format(data.config['Looks']['Icons']['Theme']), master = toolbar)
tools_looks = ttk.Button(toolbar,image=tools_looks_icon, command=togglelookpane)
tools_looks.pack(fill='x')
tools_settings_icon = PhotoImage(file = "./DATA/icons/{}/sidebar.settings.png".format(data.config['Looks']['Icons']['Theme']), master = toolbar)
tools_settings = ttk.Button(toolbar,image=tools_settings_icon, command=togglesetti)
tools_settings.pack(side='bottom',anchor='s',fill='x')

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

from tkterminal import *
termframe = ttk.Frame()
termicon_clear = PhotoImage(file= './DATA/icons/{}/terminal.clear.png'.format(data.config['Looks']['Icons']['Theme']))
termicon_reset = PhotoImage(file= './DATA/icons/{}/terminal.restart.png'.format(data.config['Looks']['Icons']['Theme']))
tkterminal = Terminal(termframe, font='Consolas 10')
tkterminal.basename = "$"
tkterminal.shell = True
newframe = tk.Frame(termframe)
newframe.pack(side='right',anchor='ne')
tkterm_clear = tk.Button(newframe,anchor='n',image=termicon_clear, relief='flat', command=lambda:tkterminal.clear())
tkterm_reset = tk.Button(newframe,anchor='n',image=termicon_reset, relief='flat', command=lambda:termreset())
tkterm_clear.pack(side='top')
tkterm_reset.pack(side='top')
tkterminal.pack(side='left',anchor='w',fill='both',expand=True)
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
	zipfile.ZipFile(themefolder+'/'+default_theme,'r').extractall(tempfile.gettempdir()+"/whTheme/")
	themefile = tempfile.gettempdir()+"/whTheme/"+read(open(tempfile.gettempdir()+"/whTheme/__init__.whirldata").read())['main'][0]
	themebase = read(open(tempfile.gettempdir()+"/whTheme/__init__.whirldata").read())['name'][0]
	thisroot.tk.call('source', themefile)
	style.theme_use(themebase)
	default_highlight = configuration['Looks']['Scheme']['Folder']+configuration['Looks']['Scheme']['Default']+'.json'
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
	if notebook.select().replace('.!panedwindow.!panedwindow.!panedwindow.!notebook.!frame','') == "":
		variable = 0
	else:
		variable = int(notebook.select().replace('.!panedwindow.!panedwindow.!panedwindow.!notebook.!frame',''))
		if variable == 0:
			pass
		else:
			variable = int(variable) -1
	return variable

def deltab(*args):
	try:
		if openedfiles[curnote2()] == "":
			notebook.forget(notebook.select())
		else:
			if open(openedfiles[curnote2()]).read() == note[curnote2()].get(1.0,END):
				notebook.forget(notebook.select())
			else:
				optionchoosen = askyesnocancel("Save file?", "Save unsaved changes in {}".format(notebook.tab(notebook.select(), "text")))
				if optionchoosen == True:
					saveFile()
				elif optionchoosen == False:
					notebook.forget(notebook.select())
				else:
					pass
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
		note[variable].insert(1.0,file.read()[:-1])
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
	note[var] = CodeEditor(frames[var],blockcursor=configuration['Looks']['Font']['BlockCursor'],width=40, height=100, language=configuration['Looks']['InitialSyntax'],autofocus=True, insertofftime=0, padx=0, pady=0, font =data.font, highlighter = default_highlight)
	note[var].pack(fill="both", expand=True)
	font = tkfont.Font(font=note[var]['font'])
	note[var].config(tabs=font.measure('    '))
	openedfiles[var] = ""
	notebook.add(frames[var], text='Untitled')
	extension[curnote()] = ".*"
	note[var].bind('<Control-Tab>',nexttab)
	note[var].bind("Control-a",select_all)
	var = var + 1
	nexttab()

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

notebook = ttk.Notebook(root)
notebook.grid(sticky = N + E + S + W)

def nexttab(*args):
	try:
		notebook.select(curnote2()+1)
	except:
		notebook.select(0)

newTab()

extension[curnote()] = ".*"

btn = ttk.Button(thisroot,text = 'NEW')
btn.place(anchor='ne')

if len(sys.argv) >= 2:
	if os.path.isfile(sys.argv[1]):
		extension[curnote()] = "."+filepath.split(".")[-1]
		note[variable].delete(1.0,END)
		file = open(filepath,"r")
		note[curnote2()]["language"] = identify(filepath.split("/")[-1])
		note[variable].insert(1.0,file.read())
		openedfiles[variable] = filepath
		file.close()
		notebook.tab(frames[variable], text = filepath.split("/")[-1])
		note[curnote2()].config(language=identify("."+filepath.split(".")[-1]))

root.add(notebook,before=termframe,height=450)

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
#<Control-Tab>
def special(*args):
	print(str(len(note[curnote2()].get(1.0,END)))+'::'+str(len(open(openedfiles[curnote2()]).read())))
thisroot.bind("<Control-Q>",special)
thisroot.bind_all('<Control-Tab>',nexttab)
notebook.bind_all('<Control-Tab>',nexttab)
thisroot.bind_all(configuration['Key Bindings']['Fullscreen'],fullscreen)
thisroot.config(menu = None)#Menubar)
thisroot.mainloop()
configs.close()
print(yaml.dump(data.config))
open('./DATA/configure.yaml','w+').write(yaml.dump(data.config))
try:
	shutil.rmtree(tempfile.gettempdir()+'/whTheme')
except:
	pass
