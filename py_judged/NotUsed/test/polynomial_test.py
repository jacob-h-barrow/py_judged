from sympy import lambdify

def test_fxn(testcase) -> bool:
    # Could differentiate or integrate, etc.
    f = lambdify(testcase.variables, testcase.equation, 'numpy')
    
    return f(*testcase.testcase_input)
