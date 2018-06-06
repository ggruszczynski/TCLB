
from SymbolicCollision.utils.sym_col_utils import *
from SymbolicCollision.utils.cm_symbols import *
from sympy.matrices import Matrix
from sympy import pretty_print, exp
from SymbolicCollision.utils.cm_symbols import ex, ey
from SymbolicCollision.utils.printers import print_as_vector_raw, print_as_vector_re
import numpy as np
from sympy.utilities.iterables import flatten

from SymbolicCollision.shift_matrix import get_shift_matrix
from SymbolicCollision.utils.cm_symbols import Shift_ortho_Geier, K_ortho_Geier, ex_Geier, ey_Geier, M_ortho_GS



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

