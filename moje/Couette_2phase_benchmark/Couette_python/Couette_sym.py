import sympy
from sympy.solvers import solve
from sympy import Symbol
# from sympy import *


u_t = Symbol('u_t')
u_m = Symbol('u_m')

mi_t = Symbol('mi_t')
mi_b = Symbol('mi_b')

H = Symbol('H')
h = Symbol('h')

solved_um = solve(mi_t*(u_t-u_m)/(H-h) - mi_b*u_m/h, u_m)

print(solved_um)

# x=Symbol('x')
# y=Symbol('y')

# expr = sin(x)/x + y
# ans2 = expr.evalf(subs={x: 3.14, y : 1})

# print ans2

# from sympy.parsing.sympy_parser import parse_exp
# sympy_exp = parse_expr(solved_um)
#
# ans2 = sympy_exp.evalf(subs={mi_t: 3.14, u_t : 1, u_m :2, H : 2, h : 1, mi_b : 4.5})
#
# print (ans2)


