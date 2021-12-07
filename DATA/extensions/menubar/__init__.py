tasks.before_mainloop.append("""
Menubar = Menu(root, activebackground="#0084FF", activeforeground="#FFFFFF",
               bg="#FFFFFF", fg="#0084FF", font="consolas")

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
viewMenu.add_command(label = "Files Pane", command = lambda:togglesidepane())
viewMenu.add_command(label = "Looks Pane", command = lambda:togglelookpane())
viewMenu.add_command(label = "Runner Pane", command = lambda:togglerunner())
viewMenu.add_command(label = "Settings Pane", command = lambda:togglesetti())
viewMenu.add_separator()
viewMenu.add_command(label = "Fullscreen", command = lambda:fullscreen())
Menubar.add_cascade(label = "Toggle", menu = viewMenu)

toolsMenu = Menu(root,tearoff=0)
confmenu = Menu(root,tearoff=0)
runmenu = Menu(root,tearoff=0)

runner_command = StringVar()
if isConf:
    for i in get_confs():
        if i != "@":
            runmenu.add("command",label = i, command = lambda i=i: runner_conf(i))
    runmenu.add_separator()
runmenu.add_command(label= "New Runner",command = lambda:new_runner())
toolsMenu.add_cascade(label = "Runner", menu = runmenu)
toolsMenu.add_command(label = "Open cmd here", command = lambda:opencmd())
Menubar.add_cascade(label="Tools",menu = toolsMenu)

syntaxMenu = Menu(root,tearoff=0)
setSyntaxMenu = Menu(root,tearoff=0)
for i in highlight.keys():
    setSyntaxMenu.add_command(label = i,command = lambda lang=i: set_syntax(lang))
#syntaxMenu.add_cascade(label = "Syntax", menu = setSyntaxMenu)
Menubar.add_cascade(label = "Syntax",menu = setSyntaxMenu)

Helpmenu = Menu(root, tearoff = 0)
Helpmenu.add_command(label = "GitHub", command=lambda:webbrowser.open("https://github.com/whmsft/WhirlEdit/"))
Helpmenu.add_separator()
#Helpmenu.add_command(label = "Changelog", command=None)
Helpmenu.add_command(label = "About",command = about)
Menubar.add_cascade(label = "Help", menu=Helpmenu)

thisroot.config(menu=Menubar)
""")
