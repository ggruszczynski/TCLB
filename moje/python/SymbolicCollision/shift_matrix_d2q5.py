
from sympy import pretty_print
from SymbolicCollision.utils.sym_col_utils import *
from SymbolicCollision.utils.cm_symbols import *

# Smat = get_shift_matrix(K_ortho_Straka_d2q5, ex_Straka_d2_q5, ey_Straka_d2_q5)
# pretty_print(Smat)

Smat = Shift_ortho_Straka_d2q5
k = get_populations('k', start=1, end=5)
Relax = diag(Symbol('w2'), Symbol('w3'), Symbol('w4'), Symbol('w5'))   #
cm_neq = get_populations('cm_neq', start=1, end=5)

k = Smat.inv()*Relax*cm_neq

pretty_print(k)
