from SymbolicCollision.cm_symbols import ux, uy
from SymbolicCollision.sym_col_utils import print_as_vector_re, print_as_vector_raw
from sympy.matrices import Matrix, diag
from sympy import Symbol, pretty_print

ex_Straka_d2_q5 = Matrix([0, -1, 0, 1, 0])
ey_Straka_d2_q5 = Matrix([0, 0, -1, 0, 1])

K_ortho_Straka_d2q5 = Matrix([  # in Geier's lattice numbering CSYS
    [1,  0,  0,  4,  0],  # 0
    [1, -1,  0, -1, -1],  # 1
    [1,  0, -1, -1,  1],  # 2
    [1,  1,  0, -1, -1],  # 3
    [1,  0,  1, -1,  1],  # 4
])


def get_cm_coeff_diag_matrix(m, n):

    def get_coeff(i, m, n):
        # coeff = pow((ex[i] - ux), m) * pow((ey[i] - uy), n)
        coeff = pow((ex_Straka_d2_q5[i] - ux), m) * pow((ey_Straka_d2_q5[i] - uy), n)
        return coeff

    diagonala = [get_coeff(i, m, n) for i in range(0, 5)]
    return diag(*diagonala)



def get_sum_of_cm_coeff_diag_matrix():
    cm_ = get_cm_coeff_diag_matrix(0, 0)
    cm_ += get_cm_coeff_diag_matrix(1, 0)  # x
    cm_ += get_cm_coeff_diag_matrix(0, 1)  # y
    cm_ += get_cm_coeff_diag_matrix(2, 0)  # xx
    cm_ += get_cm_coeff_diag_matrix(0, 2)  # yy

    return cm_


print("\n === tests ===  \n")


pretty_print(get_cm_coeff_diag_matrix(2, 0) * K_ortho_Straka_d2q5 * Matrix([1, 0, 0, 0, 0]))

# pretty_print(get_sum_of_cm_coeff_diag_matrix() * K_ortho_Straka_d2q5 * Matrix([0, 0, 0, 1, 0, 0, 0, 0, 0]) )
print_as_vector_re(get_sum_of_cm_coeff_diag_matrix()*Matrix([1, 0, 0, 0, 0]))
# print_as_vector_re(get_sum_of_cm_coeff_diag_matrix() * K_ortho_Straka_d2q5)
#

#
# pretty_print(get_sum_of_cm_coeff_diag_matrix() * K_ortho_Straka_d2q5 * Matrix([0, 0, 0, 0, 0, 1]) )