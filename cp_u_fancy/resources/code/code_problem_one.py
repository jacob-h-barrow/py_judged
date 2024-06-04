import sys
import json

from typing import Union

def func_tester(fun):
    def runner(*args, **kwargs):
        try:
            result = fun(*args, **kwargs)
        except:
            result = False
        return result
    return runner
    
@func_tester
def test_case_one(integer_list: list[int]) -> Union[bool, tuple[int, int]]:
    return [min(integer_list), len(integer_list)]

print(test_case_one(json.loads(sys.argv[1])))
sys.exit()
