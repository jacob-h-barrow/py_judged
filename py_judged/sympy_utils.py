from typing import Any, Dict, Tuple, NoReturn
from dataclasses import dataclass

import sympy as sp

type Equation = str | sp.core.relational.Equality
type Symbol = sp.core.symbol.Symbol

type Variables = Tuple[Symbol]
type Equation_Input = Tuple[Any]
type Equation_Output = int | float | Equation

type Substituting_Variables = Dict[Symbol, Any]

type Result = Equation | float | int | NoReturn

@dataclass
class SympyTestcase:
    idx: int
    equation: Equation
    variables: Variables
    testcase_input: Equation_Input
    answer: Equation_Output
