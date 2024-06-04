import tkinter as tk
import configparser
import sys

from PIL import Image, ImageTk
from tkinter import ttk

sys.path.append("/usr/Sphinx/apps/base_classes/")

from driver_frame import App

# Create a package for doing these image modifications -> code once and in one place!
class Categories(tk.Frame):
    """
        # if ctrls is a list of all lables to your checkboxes
        # i is the count and j is the text of label
        for i,j in enumerate(ctrls): #what ever loop you want
            var = IntVar()
            c = Checkbutton(self.master,text=j,variable=var)
            boxes.append([j.strip(),var,c])
            
        for i in boxes:
            if i[1].get()==0:
                #do what ever you want 
                i[2].destroy()
    """
    def __init__(self, parent, controller, category: str = ""):
        tk.Frame.__init__(self, parent)
        
        # Use category to populate the pictures/problems!
        
        self.coords_list = []
        self.buttons = {}
        self.data = {}
        
        self.on = True
        self.on_switch = Image.open('./images/on_switch.png')
        self.on_switch = ImageTk.PhotoImage(self.on_switch.resize((55,55), Image.ANTIALIAS))
        self.off_switch = Image.open('./images/off_switch.png')
        self.off_switch = ImageTk.PhotoImage(self.off_switch.resize((50,50), Image.ANTIALIAS))
        
        self.toggle_frame = ttk.LabelFrame(self, text="Switch Between Listing Interface", padding=(20, 10))
        self.toggle_frame.grid(row=0, column=0, padx=(20,10), pady=(20,10), sticky="nsew")
        
        self.toggle = ttk.Button(self.toggle_frame, image=self.on_switch, command=self.switch_view)
        self.toggle.grid(row=0, column=0, sticky="nesw")
        
        # Ex -> put off to function later
        # Also allow passed/unsuccessful
        self.data['ex_tag'] = tk.BooleanVar()
        self.tag_ex = ttk.Checkbutton(self.toggle_frame, text="Example Tag", variable=self.data['ex_tag'])
        self.tag_ex.grid(row=0, column=1, sticky="nsew")
        
        self.apply_tags = ttk.Button(self.toggle_frame, text="Apply Tags", padding=(20,10))
        self.apply_tags.grid(row=1, column=1, sticky="nesw")
        
        self.board_frame = ttk.Frame(self, padding=5)
        self.board_frame.grid(column=0, row=1, sticky="nesw")
        
        self.read_ini_file()
        
        for r in range(3):
            for c in range(2):
                coord = f"{r}_{c}"
                self.coords_list.append(coord)
                
                place = r * 2 + c + 1
                button_number = f"Button {place}"
                
                self.buttons[self.coords_list[-1]] = ttk.Button(self.board_frame, image=self.data[button_number]["img"])
                self.buttons[self.coords_list[-1]]["command"] = lambda x=c, y=r: self.fire_here(x,y)
                self.buttons[self.coords_list[-1]].grid(row=r, column=c, padx=(10,10), pady=(10,10), sticky="nesw")
                
        self.button_frame = ttk.LabelFrame(self, text="Actions", padding=(20,10))
        self.button_frame.grid(row=4, column=0, padx=(20,10), pady=(20,10), sticky="nsew")
        
        # Minimize functions by using event lambda in future!!!
        self.prev_page = ttk.Button(self.button_frame, text="Prev Page", command=self.get_prev_page)
        self.prev_page.grid(row=0, column=0, padx=(10,10), pady=(10,10), sticky="nesw")
        
        self.next_page = ttk.Button(self.button_frame, text="Next Page", command=self.get_next_page)
        self.next_page.grid(row=0, column=1, padx=(10,10), pady=(10,10), sticky="nesw")
        
        self.problem_of_the_day = ttk.Button(self.button_frame, text="Daily Problem", command=self.daily_problem)
        self.problem_of_the_day.grid(row=0, column=2, padx=(10,10), pady=(10,10), sticky="nesw")
        
        self.home_button = ttk.Button(self.button_frame, text="Go Home", command=self.go_home)
        self.home_button.grid(row=0, column=3, padx=(10,10), pady=(10,10), sticky="nesw")
        
        self.board_frame.columnconfigure(tuple(range(2)), weight=1)
        self.board_frame.rowconfigure(tuple(range(3)), weight=1)
        
    def switch_view(self):
        if self.on:
            self.toggle.config(image=self.off_switch)
        else:
            self.toggle.config(image=self.on_switch)
            
        self.on = not self.on
        
    def get_prev_page(self):
        pass
        
    def get_next_page(self):
        pass
        
    def read_ini_file(self):
        config = configparser.ConfigParser()
        # Standardize location
        config.read('./buttons.ini')
        
        for section in config.sections():
            self.data[section] = {}
            for key in config[section]:
                if key == "image":
                    # Standardize location
                    self.data[section][key] = f"./images/{config[section][key]}"
                    img = Image.open(self.data[section]["image"])
                    img = img.resize((125,125), Image.ANTIALIAS)
                    self.data[section]["img"] = ImageTk.PhotoImage(img)
                else:
                    self.data[section][key] = config[section][key]
                    
    def fire_here(self, x, y):
        place = y * 2 + x + 1
        section = f"Button {place}"
        
        try:
            print(self.data[section]["name"])
        except:
            print(f"Could not open the following: column {x}, row {y}, place {place}")
            
    def daily_problem(self):
        print("Daily problem!")
        
    def go_home(self):
        print("Going home!")
        
if __name__ == "__main__":
    root = App([Categories], Categories)
    
    root.mainloop()
