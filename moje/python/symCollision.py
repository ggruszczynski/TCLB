from sympy import Symbol
from sympy.interactive.printing import init_printing
from sympy.printing import print_ccode
from sympy.matrices import Matrix, eye, zeros, ones, diag, GramSchmidt

import re
import numpy as np
init_printing(use_unicode=False, wrap_line=False, no_global=True)


"""
M - distributions to raw moment transformation matrix
N - raw moments to central moments transformation matrix

based on:
'Modeling incompressible thermal flows using a central-moment-based lattice Boltzmann method' 
Linlin Fei, Kai Hong Luo, Chuandong Lin, Qing Li
2017
"""


# HELPERS:
def print_u2():
    ux2 = "ux2"
    print("real_t %s = %s*%s;" % (ux2, ux, ux))
    uy2 = "uy2"
    print("real_t %s = %s*%s;" % (uy2, uy, uy))
    uxuy = "uxuy"
    print("real_t %s = %s*%s;" % (uxuy, ux, uy))
    print("")


def print_as_vector_re(some_matrix, print_symbol='default_symbol1'):
    rows = some_matrix._mat
    ux2 = "ux2"
    uy2 = "uy2"
    uxuy = "uxuy"

    for i in range(len(rows)):
        row = str(rows[i])
        row = re.sub("%s\*\*2" % ux, '%s' % ux2, row)
        row = re.sub("%s\*\*2" % uy, '%s' % uy2, row)
        row = re.sub("%s\*%s" % (ux, uy), '%s' % uxuy, row)
        print("%s[%d] = %s;" % (print_symbol, i, row))
        # raw
        # print("%s[%d] = %s;" % (print_symbol, i, rows[i]))


def print_as_vector_raw(some_matrix, print_symbol='default_symbol1'):
    rows = some_matrix._mat

    for i in range(len(rows)):
        row = str(rows[i])
        print("%s[%d] = %s;" % (print_symbol, i, row))


def get_populations(print_symbol='default_symbol2'):
    symbols_ = [Symbol("%s[%d]" % (print_symbol, i)) for i in range(9)]

    return Matrix(symbols_)


def get_m00(print_symbol='default_symbol3'):
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
sb = 0.5  # results in bulk viscosity = 1/6 since : zeta = (1/sb - 0.5)*cs^2*dt

# TRANSFORMATIONS:

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

# raw moments - interpretation
# real_t m00 = f[0] + f[1] + f[2] + f[3] + f[4] + f[5] + f[6] + f[7]  + f[8];  // m00 - m0: density
# real_t m10 =        f[1]        - f[3]        + f[5] - f[6] - f[7]  + f[8];  // m10 - m1: x momentum flux
# real_t m01 =             + f[2]        - f[4] + f[5] + f[6] - f[7]  - f[8];  // m01 - m2: y momentum flux
# real_t m20 =        f[1]        + f[3]        + f[5] + f[6] + f[7]  + f[8];  // m20 - m3
# real_t m02 =               f[2]        + f[4] + f[5] + f[6] + f[7]  + f[8];  // m02 - m4
# real_t m11 =                                    f[5] - f[6] + f[7]  - f[8];  // m11 - m5: stress tensor xy (off-diagonal)
# real_t m21 =                                    f[5] + f[6] - f[7]  - f[8];  // m21 - m6
# real_t m12 =                                    f[5] + f[6] - f[7]  - f[8];  // m12 - m7
# real_t m22 =                                    f[5] + f[6] + f[7]  + f[8];  // m22 - m8

# SHIFT MATRIX
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


# RELAXATION MATRIX
s_plus = (sb+sv)/2
s_minus = (sb-sv)/2

S = diag(1, 1, 1, s_plus, s_plus, sv, 1, 1, 1)
S[3, 4] = s_minus
S[4, 3] = s_minus


force_in_cm_space = Matrix([
            0,
            Symbol('Fhydro.x'),
            Symbol('Fhydro.y'),
            0,
            0,
            0,
            Symbol('(Fhydro.y/3.)'),
            Symbol('(Fhydro.x/3.)'),
            0,
            ])

cm_eq = Matrix([Symbol('m00'),
                0,
                0,
                Symbol('(m00/3.)'),
                Symbol('(m00/3.)'),
                0,
                0,
                0,
                Symbol('(m00/9.)'),
                ])

# # ============ COLLISION all at once ;D ================
# cm = N * Mraw * f_in
# # cm_eq = N*Mraw*feq
# # cm_after_collision = (eye(9)-S)*cm + S*cm_eq + (eye(9)-S/2.)*N*Mraw*body_force  # eq 8
# cm_after_collision = (eye(9)-S)*cm + S*cm_eq + (eye(9)-S/2.)*force_in_cm_space  # eq 8
#
# # back to densities space
# f_after_collision = Mraw.inv() * N.inv()*cm_after_collision
#
# print("\n\n=== PRETTY CODE all at once ;D ===\n\n")
# print_ccode(get_m00('f_in'), assign_to='real_t m00')
# print("")
# print_u2()
# print_as_vector_re(f_after_collision, "f_out")
#
# # print("\n\nby print_ccode \n")
# # for i in range(len(f_after_collision)):
# #     print_ccode(f_after_collision[i], assign_to='f_out[%s]' % i)


# ============ COLLISION separate ================
print("\n\n=== PRETTY CODE separate ===\n\n")

pop_in_str = 'f_in'  # symbol defining populations
temp_pop_str = 'temp'  # symbol defining populations

print("CudaDeviceFunction void relax_central_moments("
      "real_t %s[9], "
      "real_t tau, "
      "vector_t Fhydro, "
      "vector_t u) \n{"
      % pop_in_str)

print_u2()
print("real_t %s = 1./tau;" % sv)

print_ccode(get_m00(pop_in_str), assign_to='real_t m00')

print("real_t %s[9];\n"
      "for (int i = 0; i < 9; i++) {\n\t"
      "%s[i] = %s[i];}" % (temp_pop_str, temp_pop_str, pop_in_str))

populations = get_populations(pop_in_str)
temp_populations = get_populations(temp_pop_str)
m = Mraw * temp_populations

print("\n//raw moments from density-probability functions")
print("//[m00, m10, m01, m20, m02, m11, m21, m12, m22]")
print_as_vector_raw(m, print_symbol=pop_in_str)

print("\n//central moments from raw moments")
cm = N * populations
print_as_vector_re(cm, print_symbol=temp_pop_str)

# print("\n\n//central moments from raw moments - by print_ccode \n")
# for i in range(len(cm)):
#     print_ccode(cm[i], assign_to='%s[%s]' % (temp_pop_str, i))

print("\n//collision in central moments space")
cm_after_collision = (eye(9)-S)*temp_populations + S*cm_eq + (eye(9)-S/2)*force_in_cm_space  # eq 8
print_as_vector_raw(cm_after_collision, print_symbol=pop_in_str)

print("\n//back to raw moments")
m = N.inv()*populations
print_as_vector_re(m, print_symbol=temp_pop_str)

# print("\n\n//back to raw moments - by print_ccode \n")
# for i in range(len(m)):
#     print_ccode(m[i], assign_to='%s[%s]' % (temp_pop_str, i))

print("\n//back to density-probability functions")
populations = Mraw.inv()*temp_populations
print_as_vector_raw(populations, print_symbol=pop_in_str)

print("\n}\n")





# // real_t F_i[9];
# // for ( int i=0; i < 9; i++){
# //         // F_i[i] = 3.0*wf[i] * (Fhydro.x*d2q9_ex[i] + Fhydro.y*d2q9_ey[i])/rho;
# //         F_i[i] = f_eq[i]*3.0*(Fhydro.x*(d2q9_ex[i]-u.x) + Fhydro.y*(d2q9_ey[i]-u.y))/rho;  // eq 11 - He et al. forcing scheme
# // }

