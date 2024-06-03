from judger_utils import Judger_Resource_Tracker
from sympy_utils import SympyTestcase
from utils import UserCode, Testcases, NormalTestcase
from runner import non_threaded_code_runner, code_tester

import sympy as sp

ex_1_tc = NormalTestcase(1, [i for i in range(20)], [i*2 for i in range(20)])
ex_1_uc = UserCode('master_code_1', './test/master_code_1.py')

judged = code_tester(ex_1_tc, ex_1_uc)

print(judged)

ex_2_tc = NormalTestcase(2, [0,1,2,3,4,5,6,7,8], [0,1,2,4,8,3,5,6,7])
ex_2_uc = UserCode('sort_by_bits', './test/sort_by_bits.py')

judged_2 = code_tester(ex_2_tc, ex_2_uc)

judged_2.passed()

print(judged_2.pp())


testcases = [[0,1,2,3,4,5,6,7,8], [1024,512,256,128,64,32,16,8,4,2,1]]
answers = [[0,1,2,4,8,3,5,6,7], [1,2,4,8,16,32,64,128,256,512,1024]]

_3_testcases = tuple(NormalTestcase(idx, item[0], item[1]) for idx, item in enumerate(zip(testcases, answers)))
ex_3_tcs = Testcases(_3_testcases)

ex_3_uc = UserCode('sort_by_bits', './test/sort_by_bits.py')

# threaded_code_runner(self, testcases, answers, code_module, code_location) -> JudgerResults:
new_results = non_threaded_code_runner(ex_3_tcs, ex_3_uc)

new_results.score()

new_results.display()

x, y, z = sp.symbols('x y z')

sympy_tc_1 = SympyTestcase(1, '2*x**3 + 3*y**3', (x, y), (1, 2), 26)
user_code = UserCode('polynomial_test', './test/polynomial_test.py')

print(code_tester(sympy_tc_1, user_code))

sympy_tc_2 = SympyTestcase(2, '2*x**3 + 3*y**3', (x, y), (1, 2), 6)
user_code = UserCode('diff_test', './test/diff_test.py')

res = code_tester(sympy_tc_2, user_code)

print(res.pp())
