from typing import Dict
from dataclasses import dataclass, field
from collections import defaultdict
from judger_utils import Judged_Testcases
from utils import Testcases

type uuid = str
# Not sure if these work for defaultdict??? Linter may flag!!!
type Attempted = Dict[uuid, int]
type Completed = Dict[uuid, bool]

def empty():
    return defaultdict(str)

# This is loaded from S3 bucket
@dataclass
class Problem:
    _id: uuid
    name: str
    description: str
    difficulty: str
    
    testcases: Testcases # iter class with SympyTestcase or NormalTestcase for now
    # Always 20 testcases length: int

    starter_code: str # Includes import code and user_function
    function_name: str # Scrap and pull out
    master_code: str
    
@dataclass
class UserSystem:
    _id: uuid # Linked to an active user
    
    problems_tried: Attempted = field(init=False, default_factory=empty)
    problems_completed: Completed = field(init=False, default_factory=empty)
    
    def update_tried(self, problem_id: uuid):
        try:
            self.problems_tried[uuid] += 1
        except:
            self.problems_tried[uuid] = 1
    
    def add(self, problem_id: uuid, option: str = 'both'):
        if option == 'both':
            try:
                self.problems_completed[uuid] += 1
            except:
                self.problems_completed[uuid] = 1
            
        self.update_tried(problem_id) 
    
@dataclass
class Submission:
    problem_id: uuid
    
    judged_testcases: Judged_Testcases
