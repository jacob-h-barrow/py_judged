from sympy import lambdify, diff

def test_fxn(testcase):
    # Could differentiate or integrate, etc.
    dx_f = diff(testcase.equation, 'x')
    f = lambdify(testcase.variables, dx_f, 'numpy')
    
    return f(*testcase.testcase_input)
