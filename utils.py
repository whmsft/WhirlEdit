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
        check_btn = ttk.Checkbutton(
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
        check_btn = ttk.Checkbutton(
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