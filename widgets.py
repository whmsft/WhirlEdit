import tkinter as tk
from tkinter import ttk

class Find(tk.Toplevel):
	"""Find whole or partial words within a text widget"""

	def __init__(self, master, text_widget):
		super().__init__(master)
		self.text = text_widget
		self.title('Find')
		self.transient(master)
		self.resizable(False, False)
		self.wm_attributes('-topmost', 'true', '-toolwindow', 'true')
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.focus_set()

		# create widgets
		lbl = ttk.Label(self, text='Find what:')
		self.text_find = ttk.Entry(self, width=30, font='consolas 10')
		self.btn_next = ttk.Button(self, text='Find Next', width=10, command=self.ask_find_match)
		self.whole_word_var = tk.IntVar()
		self.whole_word_var.set(0)
		check_btn = tk.Checkbutton(
			self,
			text='Match whole word only',
			variable=self.whole_word_var,command=self.change_match_type)

		# add widgets to window
		lbl.grid(row=0, column=0, padx=(15, 2), pady=15)
		self.text_find.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=15)
		self.btn_next.grid(row=0, column=2, sticky=tk.EW, padx=(5, 15), pady=15)
		self.text_find.focus_set()
		check_btn.grid(row=1, column=0, padx=15, pady=(5, 15), columnspan=2, sticky=tk.EW)

		# other variables
		self.chars = 0
		self.term = None
		self.start = '1.0'

		# configure text widget tags
		self.text.tag_configure('found', foreground='black', background='silver')
		self.text.tag_configure('found.focus', foreground='white', background='SystemHighlight')

		# add additional bindings
		self.bind("<Return>", self.ask_find_match)

		windowWidth, windowHeight = master.winfo_width(), master.winfo_height()
		screenWidth  = self.winfo_screenwidth()
		screenHeight = self.winfo_screenheight()
		xCordinate = int((screenWidth/2) - (windowWidth/2))
		yCordinate = int((screenHeight/2) - (windowHeight/2))

		self.geometry("+{}+{}".format(xCordinate, yCordinate))

		self.mainloop()
	def cancel(self):
		"""Cancel the request and return control to main window"""
		try:
			end = self.start
			start = self.start + f'-{self.chars}c'
			self.text.tag_delete('found', 1.0, tk.END)
			self.text.tag_delete('found.focus', 1.0, tk.END)
			self.text.tag_add(tk.SEL, start, end)
			self.text.mark_set(tk.INSERT, start)
			self.text.focus_set()
			self.destroy()
		except _tkinter.TclError:
			#just in case nothing is  to find..
			self.destroy()

	def change_match_type(self):
		"""Reset found tags when match type is changed"""
		self.term = None
		self.chars = None
		self.text.tag_remove('found', '1.0', tk.END)
		self.text.tag_remove('found.focus', '1.0', tk.END)

	def ask_find_match(self, event=None):
		"""Check for new searches, and route traffic by search types"""
		term = self.text_find.get()
		if term == '':
			return
		if self.term != term:
			self.term = term
			self.chars = len(term)
			self.text.tag_remove('found', '1.0', tk.END)
			self.route_match()
		self.highlight_next_match()

	def route_match(self):
		"""Direct to whole or partial match"""
		if self.whole_word_var.get():
			self.whole_word_matches()
		else:
			self.partial_word_matches()

	def whole_word_matches(self):
		"""Locate and tag all whole word matches"""
		start = '1.0'
		while True:
			start = self.text.search(self.term, start, stopindex=tk.END)
			if not start:
				break
			end = start + ' wordend'
			found = self.text.get(start + '-1c', end)  # whole word includes a space before
			if found == ' ' + self.term:
				self.text.tag_add('found', start, end)
			start = end

	def partial_word_matches(self):
		"""Locate and tag all partial word matches"""
		start = '1.0'
		while True:
			start = self.text.search(self.term, start, stopindex=tk.END)
			if not start:
				break
			end = start + f'+{self.chars}c'
			self.text.tag_add('found', start, end)
			start = end

	def highlight_next_match(self):
		"""Highlight the next matching word"""
		self.text.tag_remove('found.focus', '1.0', tk.END) # remove existing tag
		try:
			start, end = self.text.tag_nextrange('found', self.start, tk.END)
			self.text.tag_add('found.focus', start, end)
			self.text.mark_set(tk.INSERT, start)
			self.text.see(start)
			self.start = end
		except ValueError:
			if self.start != '1.0':
				self.start = '1.0'
				self.text.see('1.0')
				self.highlight_next_match()


class Replace(tk.Toplevel):
	"""Find and replace words within a text widget"""

	def __init__(self, master, text_widget):
		super().__init__(master)
		self.text = text_widget
		self.title('Find and Replace')
		self.transient(master)
		self.resizable(False, False)
		self.wm_attributes('-topmost', 'true', '-toolwindow', 'true')
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.focus_set()

		# create widgets
		lbl1 = ttk.Label(self, text='Find what:', anchor=tk.W)
		self.text_find = ttk.Entry(self, width=30, font='-size 10')
		self.text_find.focus_set()
		self.btn_next = ttk.Button(self, text='Find Next', width=12, command=self.ask_find_match)

		lbl2 = ttk.Label(self, text='Replace with:', anchor=tk.W)
		self.text_replace = ttk.Entry(self, width=30, font='-size 10')
		self.btn_replace = ttk.Button(self, text='Replace', width=12, command=self.find_replace_next)
		self.btn_replace_all = ttk.Button(self, text='Replace All', width=12, command=self.find_replace_all)

		self.whole_word_var = tk.IntVar()
		self.whole_word_var.set(0)
		check_btn = tk.Checkbutton(
			self,
			text='Match whole word only',
			variable=self.whole_word_var, command=self.change_match_type)

		# add widgets to window
		lbl1.grid(row=0, column=0, sticky=tk.EW, padx=(15, 2), pady=(15, 0))
		lbl2.grid(row=1, column=0, sticky=tk.EW, padx=(15, 2))
		self.text_find.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=(15, 2))
		self.text_replace.grid(row=1, column=1, sticky=tk.EW, padx=5)
		self.btn_next.grid(row=0, column=2, sticky=tk.EW, padx=(5, 15), pady=(15, 2))
		self.btn_replace.grid(row=1, column=2, sticky=tk.EW, padx=(5, 15), pady=2)
		self.btn_replace_all.grid(row=2, column=2, sticky=tk.EW, padx=(5, 15), pady=(2, 15))
		check_btn.grid(row=2, column=0, columnspan=2, sticky=tk.EW, padx=15, pady=(5, 15))

		# other variables
		self.chars = 0
		self.term = None
		self.start = '1.0'

		# configure text widget tags
		self.text.tag_configure('found', foreground='black', background='silver')
		self.text.tag_configure('found.focus', foreground='white', background='SystemHighlight')

		# add additional bindings
		self.bind("<Return>", self.ask_find_match)

		windowWidth, windowHeight = master.winfo_width(), master.winfo_height()
		screenWidth  = self.winfo_screenwidth()
		screenHeight = self.winfo_screenheight()
		xCordinate = int((screenWidth/2) - (windowWidth/2))
		yCordinate = int((screenHeight/2) - (windowHeight/2))

		self.geometry("+{}+{}".format(xCordinate, yCordinate))

	def cancel(self):
		"""Cancel the request and return control to main window"""
		try:
			end = self.start
			start = self.start + f'-{self.chars}c'
			self.text.tag_delete('found', 1.0, tk.END)
			self.text.tag_delete('found.focus', 1.0, tk.END)
			self.text.tag_add(tk.SEL, start, end)
			self.text.mark_set(tk.INSERT, start)
			self.text.focus_set()
			self.destroy()
		except _tkinter.TclError:
			#raised when there's nothing highlighted!
			self.destroy()

	def change_match_type(self):
		"""Reset found tags when match type is changed"""
		self.term = None
		self.chars = None
		self.text.tag_remove('found', '1.0', tk.END)
		self.text.tag_remove('found.focus', '1.0', tk.END)

	def ask_find_match(self, event=None):
		"""Check for new searches, and route traffic by search types"""
		term = self.text_find.get()
		if term == '':
			return
		if self.term != term:
			self.term = term
			self.chars = len(term)
			self.text.tag_remove('found', '1.0', tk.END)
			self.route_match()
		self.highlight_next_match()

	def route_match(self):
		"""Direct to whole or partial match"""
		if self.whole_word_var.get():
			self.whole_word_matches()
		else:
			self.partial_word_matches()

	def whole_word_matches(self):
		"""Locate and tag all whole word matches"""
		start = '1.0'
		while True:
			start = self.text.search(self.term, start, stopindex=tk.END)
			if not start:
				break
			end = start + ' wordend'
			found = self.text.get(start + '-1c', end)  # whole word includes a space before
			if found == ' ' + self.term:
				self.text.tag_add('found', start, end)
			start = end

	def partial_word_matches(self):
		"""Locate and tag all partial word matches"""
		start = '1.0'
		while True:
			start = self.text.search(self.term, start, stopindex=tk.END)
			if not start:
				break
			end = start + f'+{self.chars}c'
			self.text.tag_add('found', start, end)
			start = end

	def highlight_next_match(self):
		"""Highlight the next matching word"""
		self.text.tag_remove('found.focus', '1.0', tk.END) # remove existing tag
		try:
			start, end = self.text.tag_nextrange('found', self.start, tk.END)
			self.text.tag_add('found.focus', start, end)
			self.text.mark_set(tk.INSERT, start)
			self.text.see(start)
			self.start = end
		except ValueError:
			if self.start != '1.0':
				self.start = '1.0'
				self.text.see('1.0')
				self.highlight_next_match()

	def find_replace_next(self):
		"""Find the next available match and replace it"""
		old_term = self.text_find.get()
		new_term = self.text_replace.get()
		start = self.text.search(old_term, tk.INSERT, tk.END)
		try:
			self.text.replace(start, start + ' wordend', new_term)
			self.highlight_next_match()
		except tk.TclError:
			return

	def find_replace_all(self):
		"""Find all matches and replace"""
		old_term = self.text_find.get()
		new_term = self.text_replace.get()
		while True:
			start = self.text.search(old_term, '1.0', tk.END)
			if not start:
				break
			self.text.replace(start, start + ' wordend', new_term)

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

		element = self.identify(event.x, event.y)
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

class ToolTip(object):

	def __init__(self, widget):
		self.widget = widget
		self.tipwindow = None
		self.id = None
		self.x = self.y = 0
		self.text = None

	def showtip(self, text):
		"""Display text in tooltip window"""
		self.text = text
		if self.tipwindow or not self.text:
			return
		x, y, cx, cy = self.widget.bbox("insert")
		x = x + self.widget.winfo_rootx() + 57
		y = y + cy + self.widget.winfo_rooty() + 27
		self.tipwindow = tw = tk.Toplevel(self.widget)
		tw.wm_overrideredirect(1)
		tw.wm_geometry("+%d+%d" % (x, y))
		label = tk.Label(tw, text=self.text, justify=tk.LEFT,
					  fg="#101010",
					  background="#ffffe0", relief=tk.SOLID, borderwidth=1,
					  font=("Consolas", "8", "normal"))
		label.pack(ipadx=1)

	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()


def create_tool_tip(widget, text):
	tool_tip = ToolTip(widget)

	def enter(event):
		tool_tip.showtip(text)

	def leave(event):
		tool_tip.hidetip()
	widget.bind('<Enter>', enter)
	widget.bind('<Leave>', leave)

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
		if delta:  # need to delete selection otherwise we would fix the current position
			self.delete(self.position, tk.END)
		else:  # set position to end so selection starts where textentry ended
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
			self.delete(0,tk.END)
			self.insert(0,self._hits[self._hit_index])
			self.select_range(self.position,tk.END)

	def handle_keyrelease(self, event):
		"""event handler for the keyrelease event on this widget"""
		if event.keysym == "BackSpace":
			self.delete(self.index(tk.INSERT), tk.END)
			self.position = self.index(tk.END)
		if event.keysym == "Left":
			if self.position < self.index(tk.END):  # delete the selection
				self.delete(self.position, tk.END)
			else:
				self.position = self.position-1  # delete one character
				self.delete(self.position, tk.END)
		if event.keysym == "Right":
			self.position = self.index(tk.END)  # go to end (no selection)
		if event.keysym == "Down":
			self.autocomplete(1)  # cycle to next hit
		if event.keysym == "Up":
			self.autocomplete(-1)  # cycle to previous hit
		# perform normal autocomplete if event is a single key or an umlaut
		if len(event.keysym) == 1:  # or event.keysym in tkinter_umlauts:
			self.autocomplete()

class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook.TNotebook"
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

        element = self.identify(event.x, event.y)
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
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", file='./DATA/icons/close.n.png'),
            tk.PhotoImage("img_closeactive", file='./DATA/icons/close.h.png'),
            tk.PhotoImage("img_closepressed", file='./DATA/icons/close.a.png'),
        )

        style.element_create(
            "close",
            "image",
            "img_close",
            ("active", "pressed", "!disabled", "img_closepressed"),
            ("active", "!disabled", "img_closeactive"),
            border=8,
            sticky='',
        )
        style.layout(
            "CustomNotebook.TNotebook",
            [("CustomNotebook.TNotebook.client", {"sticky": "nswe"})],
        )
        style.layout(
            "CustomNotebook.TNotebook.Tab",
            [
                (
                    "CustomNotebook.TNotebook.tab",
                    {
                        "sticky": "nswe",
                        "children": [
                            (
                                "CustomNotebook.TNotebook.padding",
                                {
                                    "side": "top",
                                    "sticky": "nswe",
                                    "children": [
                                        (
                                            "CustomNotebook.TNotebook.focus",
                                            {
                                                "side": "top",
                                                "sticky": "nswe",
                                                "children": [
                                                    (
                                                        "CustomNotebook.TNotebook.label",
                                                        {"side": "left", "sticky": ''},
                                                    ),
                                                    (
                                                        "CustomNotebook.TNotebook.close",
                                                        {"side": "left", "sticky": ''},
                                                    ),
                                                ],
                                            },
                                        )
                                    ],
                                },
                            )
                        ],
                    },
                )
            ],
        )
