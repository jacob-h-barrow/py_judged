from sympy import lambdify, symbols, Eq
from typing import TypeAlias, Tuple, NoReturn, Any

import sympy as sp

Equation: TypeAlias = str | sp.core.relational.Equality
Symbol: TypeAlias = sp.core.symbol.Symbol
Variables: TypeAlias = Tuple[Symbol]
Equation_Input: TypeAlias = Tuple[Any]
Equation_Output: TypeAlias = int | float | Equation

def test_fxn(testcase_idx, equation: Equation, variables: Variables, testcase_input: Equation_Input, result: Equation_Output) -> bool:
    # Could differentiate or integrate, etc.
    f = lambdify(variables, equation, 'numpy')
    
    print(f(*testcase_input))
    
    return f(*testcase_input) == result
    
if __name__ == '__main__':
    x, y = symbols('x y')
    testcase_input = (1, 2)
    eq1 = '2*x**3 + 3*y**3'
    eq2 = 2*x**3 + 3*y**3
    result = 26
    
    print(f'Running 1: { test_fxn(1, eq1, (x, y), testcase_input, result) }')
    print(f'Running 2: { test_fxn(2, eq2, (x, y), testcase_input, result) }')
