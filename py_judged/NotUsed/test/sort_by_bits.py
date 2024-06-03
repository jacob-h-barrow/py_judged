from typing import List

def test_fxn(testcase) -> List[int]:
    return sorted([num for num in testcase.testcase_input], key=lambda x: [bin(x)[2:].count('1'), len(str(x)), x] )
