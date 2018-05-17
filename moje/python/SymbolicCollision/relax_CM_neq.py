
from SymbolicCollision.sym_col_utils import *


# ============ COLLISION separate ================
print("\n\n=== PRETTY CODE relax neq ===\n\n")


pop_in_str = 'f_neq'  # symbol defining non_eq populations: f_neq = f - f_eq
temp_pop_str = 'temp'  # symbol defining populations


# eq: -S*(cm_non_eq) - (eye(9)-S/2.)*force_in_cm_space
print("CudaDeviceFunction void relax_CM_neq("
      "real_t %s[9], "
      "real_t tau, "
      "vector_t Fhydro, "
      "vector_t u) \n{"
      % pop_in_str)

print_u2_u3()
print("real_t %s = 1./tau;" % sv)
print("real_t %s = omega_bulk;" % sb)  # s_b = 1./(3*bulk_visc + 0.5)
print("")

print_ccode(get_m00(pop_in_str), assign_to='real_t m00')

print("\nreal_t %s[9];\n"
      "for (int i = 0; i < 9; i++) {\n\t"
      "%s[i] = %s[i];}" % (temp_pop_str, temp_pop_str, pop_in_str))

populations = get_populations(pop_in_str)
temp_populations = get_populations(temp_pop_str)
m_non_eq = Mraw * temp_populations

print("\n//raw moments from density-probability functions")
print("//[m00, m10, m01, m20, m02, m11, m21, m12, m22]")
print_as_vector_raw(m_non_eq, print_symbol=pop_in_str)

print("\n//central moments from raw moments")
cm_non_eq = N * populations
print_as_vector_re(cm_non_eq, print_symbol=temp_pop_str)

# print("\n\n//central moments from raw moments - by print_ccode \n")
# for i in range(len(cm)):
#     print_ccode(cm[i], assign_to='%s[%s]' % (temp_pop_str, i))

print("\n//collision in central moments space")
cm_after_collision = -S*temp_populations + (eye(9)-S/2)*force_in_cm_space
print_as_vector_raw(cm_after_collision, print_symbol=pop_in_str)
print("\n//back to raw moments")
m = N.inv()*populations
print_as_vector_re(m, print_symbol=temp_pop_str)

# print("\n\n//back to raw moments - by print_ccode \n")
# for i in range(len(m)):
#     print_ccode(m[i], assign_to='%s[%s]' % (temp_pop_str, i))

print("\n//back to density-probability functions")
populations = Mraw.inv()*temp_populations
print_as_vector_raw(populations, print_symbol=pop_in_str)

print("\n}\n")
