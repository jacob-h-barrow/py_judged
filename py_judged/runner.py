from judger_utils import Judger_Resource_Tracker, JudgerResults
from sympy_utils import SympyTestcase
from utils import UserCode, Testcases

import importlib.util as lib_utils

type Testcase = SympyTestcase | NormalTestcase

@Judger_Resource_Tracker
def code_tester(testcase: Testcase, user_code: UserCode):
    spec = lib_utils.spec_from_file_location(user_code.code_module, user_code.code_location)
    
    loaded_code = lib_utils.module_from_spec(spec)
    
    spec.loader.exec_module(loaded_code)
    
    return loaded_code.test_fxn(testcase)
    
def non_threaded_code_runner(testcases: Testcases, user_code: UserCode) -> JudgerResults:
    return JudgerResults([code_tester(testcase, user_code) for testcase in testcases])
    
# Use threaded code later... code already written
