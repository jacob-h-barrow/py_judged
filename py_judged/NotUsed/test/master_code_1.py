import sys
import json
import time

def test_fxn(testcase):
    answers = []
    for i in testcase.testcase_input:
        answers.append(i*2)
        time.sleep(0.2)
        
    return answers
        
if __name__ == "__main__":
    print(test_fxn(sys.argv[1:]))
