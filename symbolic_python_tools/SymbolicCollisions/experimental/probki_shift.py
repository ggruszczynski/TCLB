
from sympy import Symbol
from sympy.matrices import Matrix, eye, zeros, ones, diag
from sympy import pretty_print
from SymbolicCollisions.core.sym_col_fun import *
from SymbolicCollisions.core.cm_symbols import *
from SymbolicCollisions.core.shift_matrix_d2q9 import *
from SymbolicCollisions.core.printers import *


# cm = get_populations('cm')
cm = Matrix([0.123, 0.234, 0.345, 0.456, 0.567, 0.678, 0.789, 0.890, 0.901])


ShiftMat = get_shift_matrix(M_ortho_GS, ex, ey)
ShiftMat = ShiftMat.subs({
            'u.x': 0.0123,
            'u.y': 0.0234
            })

# pretty_print(ShiftMat)
f1 = M_ortho_GS*ShiftMat.inv()*cm
print_as_vector(f1, 'f1')


print('another approach')
Nraw = Nraw.subs({
            'u.x': 0.0123,
            'u.y': 0.0234
            })

f2 = Mraw.inv()*Nraw.inv()*cm
print_as_vector(f2, 'f2')


from numpy.testing import assert_almost_equal
for i in range(0):
    assert_almost_equal(f1[i], f2[i])

