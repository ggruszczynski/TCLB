from sympy import Symbol
from sympy.interactive.printing import init_printing
from sympy.matrices import Matrix, eye, zeros, ones, diag, GramSchmidt
init_printing(use_unicode=False, wrap_line=False, no_global=True)

"""
M - distributions to raw moment transformation matrix
N - raw moment to central moments transformation matrix

based on:
'Modeling incompressible thermal flows using a central-moment-based lattice Boltzmann method' 
Linlin Fei, Kai Hong Luo, Chuandong Lin, Qing Li
2017
"""

f = Matrix([Symbol('f[0]'),
            Symbol('f[1]'),
            Symbol('f[2]'),
            Symbol('f[3]'),
            Symbol('f[4]'),
            Symbol('f[5]'),
            Symbol('f[6]'),
            Symbol('f[7]'),
            Symbol('f[8]'),
            ])

# this matrix will produce raw moments in the following order:
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


ux = Symbol('u_x')
uy = Symbol('u_y')
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

k_raw = Mraw * f  # moments


def print_matrix(some_matrix, symbol='M'):
    rows = some_matrix._mat

    for i in range(len(rows)):
        print("%s[%d] = %s;" % (symbol, i, rows[i]))


print("\n\n--- raw moments ---\n")
print_matrix(k_raw,'m')

print("\n\n--- central moments ---\n")
k_central = N*k_raw  # central moments
print_matrix(k_central, 'c')

# print(Mraw.inv())
# print_matrix(Mraw.inv())




### EXPERIMENTS

# x = Symbol('x')
# M = eye(3) * x

# Mtest = Matrix([[1,0,0], [0,0,0], [31, 32, 33]]); Mtest
#
#
#
# print(Mtest)


from sympy import MatrixSymbol, BlockMatrix, symbols, Identity, ZeroMatrix, block_collapse
# n,m,l = symbols('n m l')
# X = MatrixSymbol('X', n, n)
# Y = MatrixSymbol('Y', m ,m)
# Z = MatrixSymbol('Z', n, m)
# B = BlockMatrix([[X, Z], [ZeroMatrix(m,n), Y]])
#
# print(B)
#
#
# f0 = Symbol('f[0]')
# f1 = Symbol('f[1]')
# f2 = Symbol('f[2]')