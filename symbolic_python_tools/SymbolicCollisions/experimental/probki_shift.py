
from SymbolicCollisions.core.sym_col_fun import *
from SymbolicCollisions.core.cm_symbols import *
from SymbolicCollisions.core.cm_symbols import ex, ey
from SymbolicCollisions.core.printers import print_as_vector_re

from SymbolicCollisions.core.shift_matrix_d2q9 import get_shift_matrix
from SymbolicCollisions.core.cm_symbols import M_ortho_GS



cm = get_populations('cm_neq')

mraw = N.inv() * cm
g1 = Mraw.inv() * get_populations('mraw')
print_as_vector_re(mraw, print_symbol='mraw')
print_as_vector_re(g1, print_symbol='g1')
print_as_vector_re(N.inv() * Mraw.inv() * cm, print_symbol='g1_in_one_step')


print("=== another approach ===")
Smat = get_shift_matrix(M_ortho_GS.transpose(), ex, ey)
m_ortho = Smat * cm
g2 = M_ortho_GS.transpose()*get_populations('m_ortho')

print_as_vector_re(Smat * cm, print_symbol='m_ortho')
print_as_vector_re(g2, print_symbol='g2')
print_as_vector_re(M_ortho_GS.transpose() * Smat * cm, print_symbol='g2_in_one_step')

# print("=== compare ===")
# for r1, r2 in zip(g1, g2):
#     print_as_vector_re(Matrix([r1]), print_symbol='g1')
#     print_as_vector_re(Matrix([r2]), print_symbol='g2')
#     print()
#

