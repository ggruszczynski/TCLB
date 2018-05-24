
from SymbolicCollision.sym_col_utils import *
from SymbolicCollision.cm_symbols import *
from sympy.matrices import Matrix, diag
from sympy import Symbol, pretty_print

DF = get_populations('g')
pretty_print(M_ortho_GS*DF)


print("\n\n=== is orthogonal and orhonormal? ===\n")
pretty_print(M_ortho_GS*M_ortho_GS.transpose())
# pretty_print(K_ortho_Geier.transpose()*K_ortho_Geier)



print("\n\n=== from raw moments to ortho moments ===\n")
T = M_ortho_GS*Mraw.inv()
pretty_print(T)

print("\n\n=== relax raw moments in ortho space and go back to raw moments ===\n")
S_relax_ortho = T.inv()*S_relax*T
pretty_print(S_relax_ortho)


# print("\n\n=== normalize matrix  ===\n")
# from sklearn.preprocessing import normalize
# Column_Normalized = normalize(M_ortho_GS)#, norm='l1', axis=0)
# """axis = 0 indicates, normalize by column and if you are
# interested in row normalization just give axis = 1"""
# pretty_print(Column_Normalized*Column_Normalized.transpose())