
from SymbolicCollision.utils.sym_col_utils import *
from SymbolicCollision.utils.cm_symbols import *
from SymbolicCollision.utils.printers import print_u2, print_as_vector_raw, print_as_vector_re, print_ccode

print("\n\n=== PRETTY CODE: relax and collide ===\n\n")

pop_in_str = 'f_in'  # symbol defining populations
temp_pop_str = 'temp'  # symbol defining populations
cm_eq_pop_str = 'cm_eq'  # symbol defining populations
F_cm_str = 'F_cm'
# eq8 : (eye(9)-S)*cm + S*cm_eq + (eye(9)-S/2.)*force_in_cm_space
print("CudaDeviceFunction void relax_and_collide_CM_hydro("
      "real_t %s[9], "
      "real_t tau, "
      "vector_t u, "
      "vector_t Fhydro, "
      "real_t %s) \n{"
      % (pop_in_str, rho))

print_u2()
print("real_t %s = 1./tau;" % sv)
# print("real_t bulk_visc = 1./6. ;")
# print("real_t %s = 1./(3*bulk_visc + 0.5);" % sb)  # s_b = 0.5; works good for some reason
print("real_t %s = omega_bulk;" % sb)  # s_b = 1./(3*bulk_visc + 0.5)
print("")

print_ccode(get_m00(pop_in_str), assign_to='real_t m00')

print("\nreal_t %s[9]; real_t %s[9]; real_t %s[9];\n" % (temp_pop_str, cm_eq_pop_str, F_cm_str))
print("for (int i = 0; i < 9; i++) {\n\t"
      "%s[i] = %s[i];}" % (temp_pop_str, pop_in_str))

populations = get_populations(pop_in_str)
temp_populations = get_populations(temp_pop_str)
cm_eq = get_populations(cm_eq_pop_str)
F_cm = get_populations(F_cm_str)
m = Mraw * temp_populations

print("\n//raw moments from density-probability functions")
print("//[m00, m10, m01, m20, m02, m11, m21, m12, m22]")
print_as_vector_raw(m, print_symbol=pop_in_str)

print("\n//central moments from raw moments")
cm = N * populations
print_as_vector_re(cm, print_symbol=temp_pop_str)

print("\n//collision in central moments space")
print("//calculate equilibrium distributions in cm space")
# print_as_vector_re(get_cm_vector_from_discrete_def(get_pop_eq_hydro), cm_eq_pop_str)
print_as_vector_re(hardcoded_cm_hydro_eq, cm_eq_pop_str)  # save time
print("//calculate forces in cm space")
# print_as_vector_re(get_cm_vector_from_discrete_def(get_force_Guo_second_order), F_cm_str)
# print_as_vector_re(get_cm_vector_from_continuous_def(get_continuous_force_He_original), F_cm_str)
print_as_vector_re(hardcoded_F_cm_hydro_LB_velocity_based, F_cm_str)  # save time

print("//collide eq: (eye(9)-S)*cm + S*cm_eq + (eye(9)-S/2.)*force_in_cm_space")
cm_after_collision = (eye(9) - S_relax) * temp_populations + S_relax * cm_eq + (eye(9) - S_relax / 2) * F_cm
print_as_vector_re(cm_after_collision, print_symbol=pop_in_str)

print("\n//back to raw moments")
m = N.inv()*populations
print_as_vector_re(m, print_symbol=temp_pop_str)

print("\n//back to density-probability functions")
populations = Mraw.inv()*temp_populations
print_as_vector_raw(populations, print_symbol=pop_in_str)

print("\n}\n")
