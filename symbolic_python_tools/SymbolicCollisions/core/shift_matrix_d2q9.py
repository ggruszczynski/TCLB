
from SymbolicCollisions.core.cm_symbols import ux, uy
from SymbolicCollisions.core.sym_col_fun import round_and_simplify
from sympy.matrices import Matrix, diag


def get_cm_coeff_diag_matrix(m, n, ex_, ey_):
    N = len(ex_)
    diagonala = [pow((ex_[i] - ux), m) * pow((ey_[i] - uy), n) for i in range(0, N)]
    return diag(*diagonala)


def get_shift_matrix(K, ex_, ey_):
    """
    See 'Generalized local equilibrium in the cascaded lattice Boltzmann method' by P. Asinari, 2008
    or Incorporating forcing terms in cascaded lattice Boltzmann approach by method of central moments' by Kannan N. Premnath, Sanjoy Banerjee†, 2009
    :param K: transformation matrix, from orthogonal moments to physical DF
    :param ex_: lattice vector
    :param ey_:
    :return: the shift matrix for passing from the frame at rest to the moving frame
    """

    N = len(ex_)

    def get_row(m, n):
        def get_entry(m, n, column):
            coeff = lambda i, m_, n_: pow((ex_[i] - ux), m_) * pow((ey_[i] - uy), n_)
            entry = sum([K[i, column] * coeff(i, m, n) for i in range(0, N)])
            return round_and_simplify(entry)

        row = [get_entry(m, n, i) for i in range(0, N)]
        return row

    matrix_dict = {'d2q5': [get_row(0, 0),
                            get_row(1, 0),
                            get_row(0, 1),
                            get_row(2, 0),
                            get_row(0, 2)],

                   'd2q9': [get_row(0, 0),
                            get_row(1, 0),
                            get_row(0, 1),
                            get_row(2, 0),
                            get_row(0, 2),
                            get_row(1, 1),
                            get_row(2, 1),
                            get_row(1, 2),
                            get_row(2, 2)]
                   }

    cm_ = matrix_dict['d2q%d' % N]
    return Matrix(cm_)
