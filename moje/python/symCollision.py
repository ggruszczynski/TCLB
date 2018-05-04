from sympy import Symbol
from sympy.interactive.printing import init_printing
from sympy.printing import print_ccode
from sympy.matrices import Matrix, eye, zeros, ones, diag, GramSchmidt

import re
import numpy as np
init_printing(use_unicode=False, wrap_line=False, no_global=True)


"""
M - distributions to raw moment transformation matrix
N - raw moment to central moments transformation matrix

based on:
'Modeling incompressible thermal flows using a central-moment-based lattice Boltzmann method' 
Linlin Fei, Kai Hong Luo, Chuandong Lin, Qing Li
2017
"""


# HELPERS:
def print_as_vector(some_matrix, print_symbol='default_symbol1'):
    rows = some_matrix._mat

    ux2 = "ux2"
    print("real_t %s = %s*%s;" % (ux2, ux, ux))
    uy2 = "uy2"
    print("real_t %s = %s*%s;" % (uy2, uy, uy))
    uxuy = "uxuy"
    print("real_t %s = %s*%s;" % (uxuy, ux, uy))

    for i in range(len(rows)):
        row = str(rows[i])
        row = re.sub("%s\*\*2" % ux, '%s' % ux2, row)
        row = re.sub("%s\*\*2" % uy, '%s' % uy2, row)
        row = re.sub("%s\*%s" % (ux, uy), '%s' % uxuy, row)
        print("%s[%d] = %s;" % (print_symbol, i, row))
        # raw
        # print("%s[%d] = %s;" % (print_symbol, i, rows[i]))


def get_populations(print_symbol='default_symbol2'):
    symbols_ = [Symbol("%s[%d]" % (print_symbol, i)) for i in range(9)]

    return Matrix(symbols_)


def get_m00(print_symbol='default_symbol2'):
    m00 = Symbol("%s[%d]" % (print_symbol, 0))

    for i in range(1,9):
        m00 += Symbol("%s[%d]" % (print_symbol, i))

    return m00


# SYMBOLS:
ux = Symbol('u.x')
uy = Symbol('u.y')
f_in = get_populations('f_in')
feq = get_populations('f_eq')
# body_force = get_populations('F_i')

sv = Symbol('s_v')  # s_v = 1 /(tau + 0.5)
sb = 2.  # results in bulk viscosity = 0 since : zeta = (1/sb -0.5)*cs^2

# this matrix will produce raw moments (m=M*f) in the following order:
# [m00, m10, m01, m20, m02, m11, m21, m12, m22]
Mraw = Matrix([
            [1,  1,  1,  1,  1,  1,  1,  1,  1],
            [0,  1,  0, -1,  0,  1, -1, -1,  1],
            [0,  0,  1,  0, -1,  1,  1, -1, -1],
            [0,  1,  0,  1,  0,  1,  1,  1,  1],
            [0,  0,  1,  0,  1,  1,  1,  1,  1],
            [0,  0,  0,  0,  0,  1, -1,  1, -1],
            [0,  0,  0,  0,  0,  1,  1, -1, -1],
            [0,  0,  0,  0,  0,  1, -1, -1,  1],
            [0,  0,  0,  0,  0,  1,  1,  1,  1]
            ])


# shift matrix
N = Matrix([
            [1,                      0,           0,     0,     0,       0,     0,     0, 0],
            [-ux,                    1,           0,     0,     0,       0,     0,     0, 0],
            [-uy,                    0,           1,     0,     0,       0,     0,     0, 0],
            [ux*ux,              -2*ux,           0,     1,     0,       0,     0,     0, 0],
            [uy*uy,                  0,       -2*uy,     0,     1,       0,     0,     0, 0],
            [ux*uy,                -uy,         -ux,     0,     0,       1,     0,     0, 0],
            [-ux*ux*uy,        2*ux*uy,       ux*ux,   -uy,     0,   -2*ux,     1,     0, 0],
            [-uy*uy*ux,          uy*uy,     2*ux*uy,     0,   -ux,   -2*uy,     0,     1, 0],
            [ux*ux*uy*uy,  -2*ux*uy*uy, -2*uy*ux*ux, uy*uy, ux*ux, 4*ux*uy, -2*uy, -2*ux, 1],
            ])


# Relaxation matrix
s_plus = (sb+sv)/2
s_minus = (sb-sv)/2

S = diag(1, 1, 1, s_plus, s_plus, sv, 1, 1, 1)
S[3, 4] = s_minus
S[4, 3] = s_minus


force_in_cm_space = Matrix([0,
            Symbol('Fhydro.x'),
            Symbol('Fhydro.y'),
            0,
            0,
            0,
            Symbol('Fhydro.y/3.'),
            Symbol('Fhydro.x/3.'),
            0,
            ])


# ============ COLLISION ================
cm = N * Mraw * f_in
# cm_eq = N*Mraw*feq
cm_eq = Matrix([Symbol('m00'),
                0,
                0,
                Symbol('m00/3.'),
                Symbol('m00/3.'),
                0,
                0,
                0,
                Symbol('m00/9.'),
                ])

# cm_after_collision = (eye(9)-S)*cm + cm_eq + (eye(9)-S/2)*body_force  # eq 8
cm_after_collision = (eye(9)-S)*cm + cm_eq + force_in_cm_space  # eq 8

# back to densities space
f_after_collision = Mraw.inv() * N.inv()*cm_after_collision

print("\n\nPRETTY CODE\n\n")
print_ccode(get_m00('f_in'), assign_to='m00')
print("")
print_as_vector(f_after_collision, "f_out")

# print("\n\nby print_ccode \n")
# for i in range(len(f_after_collision)):
#     print_ccode(f_after_collision[i], assign_to='f_out[%s]' % i)
