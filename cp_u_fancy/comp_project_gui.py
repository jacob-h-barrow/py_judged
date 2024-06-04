from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkFileDialog

import tkinter.messagebox as tkMessageBox
import os
import traceback

from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

root = Tk()
root.tk.call("source", "/usr/Sphinx/themes/Azure-ttk-theme-main/azure.tcl")
root.tk.call("set_theme", "light")

variables = {}
variables['file_location'] = tk.StringVar()
variables['read_only'] = tk.BooleanVar()
variables['encrypt'] = tk.BooleanVar()

def find_file():
    path = fd.askopenfilename(title='Open a configuration file!', initialdir='/')
    
    return path[:path.rfind("/")+1]
    
def save_file():
    pass    
    
check_frame = ttk.LabelFrame(root, text="INI File Configurations", padding=(20,10))
check_frame.grid(row=0, column=0, padx=(20,10), pady=(20,10), sticky="nsew")

check_button_1 = ttk.Checkbutton(check_frame, text="Read Only", variable=variables['read_only'])
check_button_2 = ttk.Checkbutton(check_frame, text="Use Encryption", variable=variables['encrypt'])

check_button_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
check_button_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

separator = ttk.Separator(root)
separator.grid(row=1, column=0, padx=(20,10), pady=(5,0), sticky="nsew")

button_frame = ttk.LabelFrame(root, text="Save/Load Options", padding=(20,10))
button_frame.grid(row=2, column=0, padx=(20,10), pady=(20,10), sticky="nsew")

find_config_button = ttk.Button(button_frame, text="Load INI File", command=find_file)
find_config_button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

save_config_button = ttk.Button(button_frame, text="Save INI file", command=save_file)
save_config_button.grid(row=0, column=1, padx=5, pady=10)

class Editor:
    STYLE = "default"
    TITLE = "Code Submission"
    
    def __init__(self, master):
        self.root = master
        self.editor = None
        self.text = None
        self.font = ("Ubuntu", 14, "bold")
        
        self.frame = LabelFrame(self.root) #, width=200, height=200)
        self.frame.grid(row=0, column=1, padx=(20,10), pady=(5,0), sticky="nsew")
        self.add_widgets()
    
    # Horizontal scroll bar goes here as well!
    def add_widgets(self):
        self.root.title("Problem Z")
        self.yscrollbar = Scrollbar(self.frame, orient="vertical")
        self.editor = Text(self.frame, yscrollcommand=self.yscrollbar.set)
        self.editor.grid(column=1, row=0, sticky="nsew") #pack(side="left", fill="both", expand=1)
        self.editor.config(wrap="word",  # use word wrapping
                           undo=True,  # Tk 8.4
                           width=40,
                           height=15,
                           tabs='    ')
        self.editor.configure(font = self.font, tabs='    ')
        self.editor.focus()
        # self.yscrollbar.pack(side="right", fill="y")
        self.yscrollbar.grid(row=3, column=5, sticky="nsew")
        self.yscrollbar.config(command=self.editor.yview)
        # self.frame.pack(fill="both", expand=1)
        
        self.editor.bind("<Control-y>", self.redo)
        self.editor.bind("<Control-Y>", self.redo)
        self.editor.bind("<Control-Z>", self.undo)
        self.editor.bind("<Control-z>", self.undo)
        self.editor.bind("<KeyRelease>", self.syntax_highlight_update)

        self.syntax_highlight_init()
        # No menu
        
    def syntax_highlight_init(self):
        style = get_style_by_name(self.STYLE)
        for t, s in style:
            name = str(t)
            for k,v in s.items():
                if k == "color" and v:
                    self.editor.tag_configure(name, foreground="#{}".format(v))
                elif k == "bgcolor" and v:
                    pass # self.editor.tag_configure(name, background="#{}".format(v))
        
    def syntax_highlight_update(self, event=None):
        self.editor.mark_set("range_start", "1.0")
        data = self.editor.get("1.0", "end-1c")
        
        for token, content in lex(data, PythonLexer()):
            self.editor.mark_set("range_end", "range_start + %dc" % len(content))
            self.editor.tag_add(str(token), "range_start", "range_end")
            self.editor.mark_set("range_start", "range_end")
            
    """
    def add_text(self):
        self.text = Text(self.root, wrap="none", width=50, height = 100, tabs='    ')
        xscrollbar = Scrollbar(self.root, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)

        yscrollbar = Scrollbar(self.root)
        yscrollbar.pack(side=RIGHT, fill=Y)

        self.text.config(
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set)
        xscrollbar.config(command=self.text.yview)
        yscrollbar.config(command=self.text.xview)

        self.text.pack()
    """
    
    def undo(self, event = None):
        self.editor.edit_undo()
        
    def redo(self, event = None):
        self.editor.edit_redo()
        
    def edit_copy(self):
        text = self.editor.get(SEL_FIRST, SEL_LAST)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def edit_paste(self):
        self.editor.insert(INSERT, root.clipboard_get())

Editor(root)

root.mainloop()
