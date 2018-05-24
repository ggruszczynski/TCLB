
from SymbolicCollision.cm_symbols import *
from SymbolicCollision.sym_col_utils import print_as_vector_raw, print_as_vector_re, get_populations, get_discrete_cm, get_gamma
from sympy import pretty_print

ex_Geier = Matrix([0, -1, -1, -1, 0, 1, 1, 1, 0])
ey_Geier = Matrix([0, 1, 0, -1, -1, -1, 0, 1, 1])



def get_cm_coeff_diag_matrix(m, n):

    def get_coeff(i, m, n):
        # coeff = pow((ex[i] - ux), m) * pow((ey[i] - uy), n)
        coeff = pow((ex_Geier[i] - ux), m) * pow((ey_Geier[i] - uy), n)
        return coeff

    diagonala = [get_coeff(i, m, n) for i in range(0, 9)]
    return diag(*diagonala)


# m = get_cm_coeff_diag_matrix(1, 0)
# DF = get_populations('f')
# pretty_print(m)
# pretty_print(m*DF)


def get_sum_of_cm_coeff_diag_matrix():
    cm_ = get_cm_coeff_diag_matrix(0, 0)
    cm_ += get_cm_coeff_diag_matrix(1, 0)  # x
    cm_ += get_cm_coeff_diag_matrix(0, 1)  # y
    cm_ += get_cm_coeff_diag_matrix(2, 0)  # xx
    cm_ += get_cm_coeff_diag_matrix(0, 2)  # yy
    cm_ += get_cm_coeff_diag_matrix(1, 1)  # xy
    cm_ += get_cm_coeff_diag_matrix(2, 1)  # xxy
    cm_ += get_cm_coeff_diag_matrix(1, 2)  # xyy
    cm_ += get_cm_coeff_diag_matrix(2, 2)  # xxyy

    return cm_


# psi = get_sum_of_cm_coeff_diag_matrix()
# print("\n === psi === \n")
# pretty_print(psi*K_ortho_Geier)
# print_as_vector_re(psi*K_ortho_Geier)
# # xsum = sum(x)

print("\n === tests ===  \n")


pretty_print(get_cm_coeff_diag_matrix(2, 0) * K_ortho_Geier * Matrix([0, 0, 0, 1, 0, 0, 0, 0, 0]))
pretty_print(get_sum_of_cm_coeff_diag_matrix() * K_ortho_Geier * Matrix([0, 0, 0, 1, 0, 0, 0, 0, 0]))
print_as_vector_re(get_sum_of_cm_coeff_diag_matrix() * K_ortho_Geier * Matrix([0, 0, 0, Symbol('f'), 0, 0, 0, 0, 0]))
