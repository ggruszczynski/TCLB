
from SymbolicCollision.utils.sym_col_utils import *
from SymbolicCollision.utils.cm_symbols import *
from SymbolicCollision.utils.printers import print_u2, print_as_vector_raw, print_as_vector_re, print_ccode

print("\n\n=== PRETTY CODE: relax relax_MRT_orthoGS ===\n\n")

DF_in_str = 'f_in'  # symbol defining DF
mom_DF_str = 'm'

print("CudaDeviceFunction void relax_MRT_orthoGS("
      "real_t %s[9], "
      "real_t tau, "
      "\n{"
      % DF_in_str)


print("real_t %s = 1./tau;" % sv)
print("\nreal_t %s[9]; \n" % mom_DF_str)

DF = get_populations(DF_in_str)
m_DF = get_populations(mom_DF_str)
m = M_ortho_GS * DF

print("\n//orthogonal moments from density-probability functions")
print("//[m00, energy, energy^2, "
      "x momentum flux, x energy flux, "
      "y momentum flux, y energy flux, "
      "stress tensor (diagonal), stress tensor (off-diagonal)]")
print_as_vector_raw(m, print_symbol=mom_DF_str)

print("\n//collision in orthogonal moments space")
print_as_vector_raw(S_relax_MRT_GS * m_DF, print_symbol=mom_DF_str)

print("\n//back to density-probability functions")
DF = M_ortho_GS.inv() * m_DF
print_as_vector_raw(DF, print_symbol=DF_in_str)

print("\n}\n")
