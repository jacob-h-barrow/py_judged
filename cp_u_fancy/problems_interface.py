import tkinter as tk
import configparser
import sys

from PIL import Image, ImageTk
from tkinter import ttk

class Categories:
    def __init__(self, root):        
        self.board_frame = ttk.Frame(root, padding=5)
        self.board_frame.grid(column=0, row=0, sticky="nesw")
        
        self.coords_list = []
        self.buttons = {}
        self.data = {}
        
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
                
        self.problem_of_the_day = ttk.Button(self.board_frame, text="Daily Problem", command=self.daily_problem)
        self.problem_of_the_day.grid(row=3, column=0, padx=(10,10), pady=(10,10), sticky="nesw")
        
        self.home_button = ttk.Button(self.board_frame, text="Go Home", command=self.go_home)
        self.home_button.grid(row=3, column=1, padx=(10,10), pady=(10,10), sticky="nesw")
        
        self.board_frame.columnconfigure(tuple(range(2)), weight=1)
        self.board_frame.rowconfigure(tuple(range(3)), weight=1)
        
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
