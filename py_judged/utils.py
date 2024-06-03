from sympy_utils import SympyTestcase
from typing import Any, Tuple
from dataclasses import dataclass

type Testcase = SympyTestcase | NormalTestcase

@dataclass
class NormalTestcase:
    idx: int
    testcase_input: Tuple[Any]
    answer: Tuple[Any]
    
@dataclass
class UserCode:
    code_module: str
    code_location: str
    
# Only used in runner
class Testcases:
    def __init__(self, testcases: Tuple[Testcase]):
        self.data = testcases
        self.idx = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            self.idx += 1
            return self.data[self.idx - 1]
        except:
            raise StopIteration()
            
    def __str__(self):
        return str(self.data)
