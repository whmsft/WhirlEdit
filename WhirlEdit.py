#[![Made with Python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
import os
import yaml
import subprocess
import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkfont
from WhirlData import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

filepath = ""

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
	if notebook.select().replace(".!customtext","") == "":
		variable = 0
	else:
		variable = int(notebook.select().replace(".!customtext",""))
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
		print(1)
		configs.writelines(datafile+'\n{}::["{}"::"{}"]'.format(name.get(),extension[curnote()],entry.get()))
		print(thisconf)
		conf.quit()
	def switchFunction():
		if gui.get():
			switch.config(text='Console')
		else:
			switch.config(text='No Console')
	conf = tk.Toplevel(root)
	conf.iconbitmap(r"favicon.ico")
	conf.resizable(False, False)
	conf.title("Configure runner for {} files".format(extension[curnote()]))
	conf.geometry("400x200")
	gui = BooleanVar()
	label = Label(conf,text = "Runner Name", font = "consolas")
	name = ttk.Entry(conf,width = 22, font = "consolas")
	name.place(x = 150, y = 10)
	label.place(x=10,y=16)
	#switch = ttk.Checkbutton(conf, text='Console', variable=gui, state = tk.DISABLED)
	#switch.invoke()
	#switch.config(command=switchFunction)
	label = Label(conf,text = "Command", font = "consolas")
	label.place(x=10,y=55)
	entry = AutocompleteEntry(conf,width = 22, font = "consolas")
	entry.set_completion_list((u'$file', u'$base', u'$dir', u'/k'))
	entry.place(x=150, y=50)
	entry.insert(0, 'compiler -o $base $file')
	submit = ttk.Button(conf,text = "Confirm", command = lambda:done())
	submit.place(x=150,y=150)
	conf.mainloop()

def runconf(*args):
	for i in datafile.split("\n"):
		if "[{}::".format(extension[curnote()]) in i:
			cmd = read(datafile)
			command = cmds[thisType][1]
			command.replace("$file",'"'+filepath+'"')
			base = filepath.split("/")[-1]
			base = base[:base.find(".")]
			command = command.replace("$base",base.replace(" ","_"))
			command = command.replace("$dir",'"'+"/".join(filepath.split("/")[:-1])+'"')
			subprocess.call("start cmd /k {}".format(command), shell = True)

root = tk.Tk()
root.iconbitmap(r"favicon.ico")
root.title('WhirlEdit 2bx')
windowWidth = 800
windowHeight = 530
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))

style = ttk.Style(root)
root.tk.call('source', '.\\Themes\\azure-dark.tcl')
style.theme_use('azure-dark') #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative','azure-dark')

note = {}
openedfiles = {}
var = 0

def opencmd(*args):
	try:
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

'''def Highlight(event):
	note[curnote()].tag_remove("found", "1.0", "end")
	for i in colors:
		string = "{}".format(i)
		if string:
			idx = "1.0"
			while True:
				idx = note[curnote()].search(string, idx, nocase=1, stopindex=END)
				if not idx:
					break
				lastidx = f"{idx}+{len(string)}c"
				note[curnote()].tag_add("found", idx, lastidx)
				idx = lastidx
			note[curnote()].tag_config("found", foreground="#66d9ef") # #66D9EF #F92672 #AE81FF
		idx = "1.0"	
'''

def curnote():
	variable = notebook.select()
	if notebook.select().replace(".!customtext","") == "":
		variable = 0
	else:
		variable = notebook.select().replace(".!customtext","")
	return variable

def deltab(*args):
	try:
		notebook.forget(notebook.select())
	except:
		root.quit()

def saveAsFile(*args):
	global notebook
	global extension
	global filepath
	filepath = asksaveasfilename(defaultextension="",filetypes=[ ("All Files", "*.*"),("Text Files", "*.txt")])
	if not filepath:
		return
	with open(filepath, "w") as output_file:
		extension[curnote()] = "."+filepath.split(".")[-1]
		variable = curnote2()
		text = note[variable].get(1.0, tk.END)
		output_file.write(text)
	notebook.tab(note[variable], text = filepath)

def saveFile(*args):
	global notebook
	global extension
	print(curnote())
	print(openedfiles)
	if notebook.select().replace(".!customtext","") == "":
		variable = 0
	else:
		variable = notebook.select().replace(".!customtext","")
		if variable == 0:
			pass
		else:
			variable = int(variable) -1

	variable = curnote2()

	if openedfiles[variable] == "":
		saveAsFile()
	else:
		with open(openedfiles[variable], "w") as output_file:
			extension[curnote()] = "."+openedfiles[variable].split(".")[-1]


			text = note[variable].get(1.0, tk.END)
			output_file.write(text)
			notebook.tab(note[variable], text = openedfiles[curnote()])

def openFile(*self): 
	#print("a",notebook.select())
	global extension
	global filepath
	if notebook.select() == "":
		newTab()

	variable = curnote2()
	filepath = askopenfilename(defaultextension=".py", filetypes=[("All Files","*.*"), ("Text Documents","*.txt"),("Python Files","*.py")]) 
	if filepath == "": 
		filepath = None
	else: 
		extension[curnote()] = "."+filepath.split(".")[-1]
		print(extension)
		note[variable].delete(1.0,END) 
		file = open(filepath,"r") 
		note[variable].insert(1.0,file.read()) 
		openedfiles[variable] = filepath
		file.close() 
		notebook.tab(note[variable], text = filepath)

def newTab(*args):
	global var
	global notebook
	note[var] = CustomText(font = "consolas", relief = FLAT)# background = "#2e2e2e", foreground = "white"
	note[var].grid(sticky = N+E+S+W)
	note[var].focus_set()
	font = tkfont.Font(font=note[var]['font'])
	note[var].config(tabs=font.measure('    '))
	openedfiles[var] = ""
	notebook.add(note[var], text='Untitled')
	extension[curnote()] = ".*"
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
Filemenu.add_command(label="Exit", command=root.destroy)
Menubar.add_cascade(label="File", menu=Filemenu)

toolsMenu = Menu(root,tearoff=0)
confmenu = Menu(root,tearoff=0)
runmenu = Menu(root,tearoff = 0)
runmenu.add_command(label = "Open file from cmd", command = lambda:runfile())
runmenu.add_separator()
runner_command = StringVar()
if isConf:
	for i in getConfs():
		runmenu.add("command",label = i, command = lambda i=i: runnerConf(i))
	runmenu.add_separator()
runmenu.add_command(label= "New Runner",command = lambda:newrunner())
toolsMenu.add_cascade(label = "Runner", menu = runmenu)
toolsMenu.add_command(label = "Open cmd here", command = lambda:opencmd())
Menubar.add_cascade(label="Tools",menu = toolsMenu)

#Helpmenu = Menu(root, tearoff = 0)
#Helpmenu.add_command(label = "Website", command=lambda:webbrowser.open("http://www.github.com/Whirlpool-Programmer/WhirlEdit/"))
#Helpmenu.add_separator()
#Helpmenu.add_command(label = "Changelog", command=None)
#Helpmenu.add_command(label = "About",command = None)
#Menubar.add_cascade(label = "Help", menu=Helpmenu)

root.grid_rowconfigure(0, weight=1) 
root.grid_columnconfigure(0, weight=1) 

line = StringVar()

notebook = ttk.Notebook(root)
notebook.grid(sticky = N + E + S + W)
newTab()

extension[curnote()] = ".*"
notebook.bind("<Double-Button>", newTab)
root.bind("<Control-s>", saveFile)
root.bind("<Control-n>", newTab)
root.bind("<Control-w>", deltab)
root.bind("<Control-o>", openFile)
root.bind("<Control-F5>",runfile)
root.bind("<F5>",runconf)
root.bind("<Control-Shift-T>", opencmd)
#root.bind("<<TextModified>>", Highlight)
root.config(menu = Menubar)
root.mainloop()
configs.close()
