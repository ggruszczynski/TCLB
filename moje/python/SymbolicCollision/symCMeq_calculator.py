from SymbolicCollision.sym_col_utils import *
from sympy import simplify, Float, preorder_traversal


def get_e():
    symbols_ = [Matrix([ex[i], ey[i]]) for i in range(9)]

    return Matrix([symbols_])


def get_gamma(i):
    cs2 = 1./3.
    # cs2 = Symbol('cs2')
    eu = ex[i] * ux + ey[i] * uy
    u2 = ux * ux + uy * uy
    gamma = w[i] * (1 + eu / cs2 + eu * eu / (2 * cs2 * cs2) - u2 / (2 * cs2))
    return gamma


def get_pop_eq(i):
    gamma = get_gamma(i)
    g = p_star * w[i] + gamma - w[i]
    return g


def get_cm_eq(m, n):
    k = 0
    for i in range(9):
        pop = get_pop_eq(i)
        k += pow((ex[i] - ux), m) * pow((ey[i] - uy), n) * pop

    k = simplify(k)
    k_rounded = k

    for a in preorder_traversal(k):
        if isinstance(a, Float):
            k_rounded = k_rounded.subs(a, round(a, 15))

    return simplify(k_rounded)


def get_cm_eq_vector():
    cm_eq = [get_cm_eq(0, 0),
             get_cm_eq(1, 0),
             get_cm_eq(0, 1),
             get_cm_eq(2, 0),
             get_cm_eq(0, 2),
             get_cm_eq(1, 1),
             get_cm_eq(2, 1),
             get_cm_eq(1, 2),
             get_cm_eq(2, 2)
             ]
    return Matrix([cm_eq])


print('// cm_eq\n ')
cm_eq = get_cm_eq_vector()
print_as_vector_re(cm_eq, 'cm_eq')
print('\n\n ')
