from utils import Testcase
from typing import Any, Tuple
from dataclasses import dataclass

import json
import time
import tracemalloc

type Judged_Testcase = Tuple[int, JudgerResult]
type Judged_Testcases = Tuple[Judged_Testcase]

@dataclass(frozen=False)
class JudgerResult:
    testcase: Testcase
    result: Any
    real_time: float
    cpu_time: float
    current_memory_blocks: float # KiB
    peak_memory_blocks: float    # KiB

    def __str__(self):
        res = f"You { 'failed' if self.failed() else 'passed' } the { self.testcase.idx } testcase!\n"
        res += f'Your solution ran with { self.current_memory_blocks } memory blocks (KiB) in { self.real_time } time'
        return res
    
    def failed(self):
        return self.result != self.testcase.answer
    
    def passed(self):
        return not self.failed()
    
    def pp(self, indent: int = 4) -> str:
        base_data = {'passed': self.passed(), 'testcase number': self.testcase.idx, 'time': self.real_time, 'peak_memory': self.peak_memory_blocks }
        
        if not base_data['passed']:
            base_data['testcase_result'] = self.result
            base_data['testcase_expected'] = self.testcase.answer
            
        return json.dumps(base_data, indent=indent)
        
@dataclass(frozen=False)
class JudgerResults:
    judged_testcases: Judged_Testcases
    
    def __post_init__(self):
        self.length = len(self.judged_testcases)
        self.total_time, total_memory = self.add_up()
        
    def add_up(self):
        total_time = total_memory = 0
        
        for judger_result in self.judged_testcases:
            total_time += judger_result.cpu_time
            total_memory += judger_result.peak_memory_blocks
            
        return total_time, total_memory
    
    def failed(self):
        return [(judger_result.testcase_idx, judger_result) for judger_result in self.judged_testcases if judger_result.failed()]
    
    def score(self):
        return (self.length - len(self.failed())) / self.length * 100
    
    def display(self):
        energy = 0
        
        print("Here are your testcases")
        for testcase in sorted(self.judged_testcases, key=lambda x: x.testcase.idx):
            print(testcase.pp(indent=4))
        
class Judger_Resource_Tracker:
    def __init__(self, func):
        self.func = func
        
    def __call__(self, *args, **kwargs):
        start = time.perf_counter(), time.process_time()
        tracemalloc.start()
        
        result = self.func(*args, **kwargs)

        current_blocks, peak_blocks = tracemalloc.get_traced_memory()
        end = time.perf_counter(), time.process_time()

        return JudgerResult(args[0], result, end[0] - start[0], end[1] - start[1], current_blocks, peak_blocks)
