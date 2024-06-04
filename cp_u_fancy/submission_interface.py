import tkinter as tk
from tkinter import ttk

import tkinter.messagebox as messagebox
from tkVideoPlayer import TkinterVideo

import tempfile
import os
import subprocess
import sys
import uuid

sys.path.append("/home/optimus/Desktop/PoTKential/components")

from editor_frame import Editor
from bullet_points import BulletFrame
from accordion_frame import Accordion
from rich_text import RichText

sys.path.append("/home/optimus/Desktop/PoTKential/CompProject/")

from runner import Runner

class SubmissionInterface:
    def __init__(self, root, information: dict):
        self.information = information
        self.interface_frame = ttk.Frame(root, padding=5)
        self.variables = {}
        
        ##############################
        ####  Editor (Top Right)  ####
        ##############################
        self.editor_frame = Editor(self.interface_frame, starter_text = self.information['function_signature'])
        self.editor_frame.set_grid(_row=0, _column=1)
        
        self.first_tab_group()
        self.second_tab_group()
        self.button_group()
        self.accordion_group()
        
        # bound accordion in function
    
    def set_grid(self, _row: int = 0, _column: int = 0):
        self.interface_frame.grid(row=_row, column=_column)
        
    ##################################
    ####  Tab group (Upper Left)  ####
    ##################################
    #####################################################################
    ####  Problem, test cases, solution, link to top user solutions  ####
    #####################################################################
    def first_tab_group(self):
        first_paned_group = ttk.PanedWindow(self.interface_frame)
        first_paned_group.grid(row=0, column=0, pady=(25,5), sticky="nsew")
        
        pane_1 = ttk.Frame(first_paned_group)
        first_paned_group.add(pane_1, weight=3)
        
        notebook = ttk.Notebook(pane_1)
        notebook.grid(row=0, column=0)
        
        tab_1 = ttk.Frame(notebook)
        notebook.add(tab_1, text="Problem Description")
        
        problem_text = RichText(20, tab_1, width=40, height=15)
        problem_text.pack(fill="both", expand=True)
        
        problem_text.insert("end", self.information['problem_description_heading'] + "\n", "h1")
        problem_text.insert("end", self.information['problem_description_heading'])
        
        tab_2 = ttk.Frame(notebook)
        notebook.add(tab_2, text="Test Cases")
        
        testcase_heading = ttk.Label(tab_2, text=self.information['testcase_heading']) 
        bullets = BulletFrame(tab_2)
        
        for testcase in self.information['testcases']:
            # Bake in a test case __str__ method -> create a class
            bullets.add_bullet(testcase)
        
        testcase_heading.grid(row=0, column=0)
        bullets.set_grid(_row=1, _column=0)
        
        tab_3 = ttk.Frame(notebook)
        notebook.add(tab_3, text="Video Solution")
        
        videoplayer = TkinterVideo(master=tab_3, scaled=True)
        videoplayer.load(r"/home/optimus/Desktop/PoTKential/testing/abs_workout.mp4")
        videoplayer.pack(side="top", fill="both", expand="True", padx=10, pady=10)
        
        # Add the videoplayer frame here -> need to create this!
        videoplayer.play()
        
        tab_4 = ttk.Frame(notebook)
        notebook.add(tab_4, text="Top User Solutions")
        
        user_solutions_heading = ttk.Label(tab_4, text=self.information['top_user_solutions_heading'])
        
        # Open in a new window for now
        # Need a separate one for each link!!!
        # Dont do anything at the moment
        user_solutions_links = ttk.Label(tab_4, text="Top Solutions Placeholder", cursor="hand2", foreground="green")
        """
            link = "XYZ"
            user_solutions_links.bind("<Button-1>", lambda e: open_solution(link))
        """
        
        user_solutions_heading.grid(row=0, column=0)
        user_solutions_links.grid(row=0, column=0)
        
    ###################################
    ####  Tab group (Middle Left)  ####
    ###################################
    #####################################################################################
    ####  Metrics on problem, link to real life related topics, experience expected  ####
    #####################################################################################
    def second_tab_group(self):
        second_paned_group = ttk.PanedWindow(self.interface_frame)
        second_paned_group.grid(row=1, column=0, pady=(25,5), sticky="nsew")
        
        pane_2 = ttk.Frame(second_paned_group)
        second_paned_group.add(pane_2, weight=3)
        
        notebook = ttk.Notebook(pane_2)
        notebook.grid(row=0, column=0)
        
        tab_1 = ttk.Frame(notebook)
        notebook.add(tab_1, text="Metrics on problem")
        
        metrics_text = RichText(10, tab_1, width=40, height=15)
        metrics_text.pack(fill="both", expand=True)
        
        metrics_text.insert("end", self.information['metrics_heading'] + "\n", "h1")
        metrics_text.insert("end", self.information['metrics_formatted'])
        
        tab_2 = ttk.Frame(notebook)
        notebook.add(tab_2, text="Related Topics")
        
        tab_3 = ttk.Frame(notebook)
        notebook.add(tab_3, text="Experience Expected")     
        
    def submit(self):        
        temp_file_location = f"/tmp/{uuid.uuid4()}.py"
        
        mypy_result = False
        pylint_result = False
        pylint_score = None
        radon_result = False
        radon_score = None
        testcases_result = None
        
        # Insert function_signature into text editor on load!!!
        code = self.get_code()
        
        function_signature = self.information['function_signature']
        function_name = self.information['function_name']
        
        with open(temp_file_location, "w") as writer:
            first_part = 'import json\nimport sys\nfrom typing import Union\ndef func_tester(fun):\n    def runner(*args, **kwargs):\n        try:\n            result = fun(*args, **kwargs)\n        except:\n            result = None\n        return result\n    return runner\n'
            last_part = f"\n\nprint({function_name}(*[json.loads(arg) for arg in sys.argv[1:]]))\nsys.exit()"
            new_code = f"{first_part}{code}{last_part}"
            print(new_code)
            writer.write(new_code)
        
        try:                
            mypy_result = subprocess.run(['mypy', "--warn-no-return", temp_file_location], capture_output=True, timeout=5).stdout.decode().strip() 
            
            if "Success: no issues found" in mypy_result:
                mypy_result = "Successful"
        except Exception as e:
            print(e)
            
        try:
            pylint_result = subprocess.run(['pylint', temp_file_location], capture_output=True, timeout=5).stdout.decode().strip()
            # Use later
            pylint_score = pylint_result.split('\n')[-1].split()[-1]
        except Exception as e:
            print(e)
            
        try:
            radon_result = subprocess.run(['radon', 'cc', temp_file_location, '--total-average'], capture_output=True, timeout=5).stdout.decode().strip()
            radon_score = radon_result.split('\n')[-1].split()[-1][1:-1]
        except Exception as e:
            print(e)
                 
        if mypy_result != "Successful":
            print(mypy_result)
        elif pylint_score == None:
            print(pylint_result)
        elif radon_score == None:
            print(radon_result)
        else:
            print(f"Scores: pylint {pylint_score}, radon {radon_score}")
            print("Now send to runner!")
        
            try:
                testcases_result = self.run_code(self.information['test_case_location'], temp_file_location, self.information['answers_location'])
                print(testcases_result)
            except Exception as e:
                print(e)

        if testcases_result:
            # Add extensions later!!!
            messagebox.showinfo("Champion!", "You solved this problem!!!")
        os.remove(temp_file_location)
        
    def hint(self):
        # messagebox
        pass    
        
    def solution(self):
        # insert text into the editor
        pass
        
    #####################################
    ####  Button group (Lower Left)  ####
    #####################################
    ######################################################################
    ####  Submit, hint, solution (lose points for hint and solution)  ####
    ######################################################################
    def button_group(self):
        button_frame = ttk.LabelFrame(self.interface_frame)
        button_frame.grid(row=1, column=1)
        
        submit_button = ttk.Button(button_frame, text="Submit", command=self.submit)
        hint_button = ttk.Button(button_frame, text="Hint (5 Pts)", command=self.hint)
        solution_button = ttk.Button(button_frame, text="Solution (15 Pts)", command=self.solution)
        
        cpane = Accordion(button_frame, 'Submission Test Cases', 'Results')
        cpane.grid(row = 1, column=0, columnspan=2, pady=15)
        
        b1 = ttk.Button(cpane.frame, text="Test Cases Result").grid(row=2, column=2, pady=10)
        cb1 = tk.Button(cpane.frame, text="Test Case One", bg="green")
        cb1.grid(row=3, column=3, pady=10)
        cb2 = tk.Button(cpane.frame, text="Test Case Two", bg="red")
        cb2.grid(row=4, column=3, pady=10)
        
        cb1.config(bg="blue")
        
        submit_button.grid(row=0, column=0, padx=5, pady=5)
        hint_button.grid(row=0, column=1, padx=5, pady=5)
        solution_button.grid(row=0, column=2, padx=5, pady=5)
        
        
    ####################################
    ####  Accordion (Bottom Right)  ####
    ####################################
    #############################################################
    ####  Submission with the test cases that passed/failed  ####
    ####                                                     #####
    ####  View submission test case for negative points (HR)  ####
    ####                               ###########################
    ####  Speed and memory comparison  ####
    #######################################
    def accordion_group(self):
        pass
        
    # bind accordion to button_submit
    def populate_accordion_group(self):
        # results = self.run_code()
        # CollaspiblePane here!
        pass        
        
    def get_code(self):
        return self.editor_frame.get_text()
        
    # Decorate was for fun!! @pylint_dynamic_code
    def run_code(self, test_case_location, temp_file_location, answers_location):
        test_result = None
        
        try:
            runner = Runner(test_case_location, temp_file_location, answers_location)
            test_case_indices = [0, 1, 2]
            
            # Modify the runner code to take a blank/empty list to mean all test indices
            test_result = runner.test_cases(test_case_indices) 
        except Exception as e:
            print(e)
            
        # Interpret results or better yet post them in the accordian below!!!
        return test_result
        


if __name__ == "__main__":
    root = tk.Tk()
    root.tk.call("source", "/usr/Sphinx/themes/Azure-ttk-theme-main/azure.tcl")
    root.tk.call("set_theme", "light")
    
    information = {"problem_description_heading": "Problem 1", "problem_description": "Placeholder for the description of problem 1", "testcase_heading": "Test Cases", "testcases": "TESTCASES", "metrics_heading": "Problem 1 Metrics", "metrics_formatted": "METRICS HERE!", "top_user_solutions_heading": "User Solutions", "test_case_location": "/home/optimus/Desktop/PoTKential/CompProject/test_cases/test_case_problem_1.txt", "answers_location": "/home/optimus/Desktop/PoTKential/CompProject/answers/answers_problem_1.txt", "function_signature": "@func_tester\ndef function(arg_list: list[int]) -> Union[bool, list[int]]:\n\t", "function_name": "function"}
    
    submission_interface = SubmissionInterface(root, information)
    
    submission_interface.set_grid()

    root.mainloop()
