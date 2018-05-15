
from SymbolicCollision.sym_col_utils import *




# ============ COLLISION separate ================
print("\n\n=== PRETTY CODE relax eq ===\n\n")

pop_in_str = 'f_in'  # symbol defining populations
temp_pop_str = 'temp'  # symbol defining populations


# eq: -S*(cm - cm_eq) - (eye(9)-S/2.)*force_in_cm_space
print("CudaDeviceFunction void relax_CM("
      "real_t %s[9], "
      "real_t tau, "
      "vector_t Fhydro, "
      "vector_t u) \n{"
      % pop_in_str)

print_u2()
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
cm_after_collision = -S*(temp_populations - cm_eq) + (eye(9)-S/2)*force_in_cm_space
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




























# # ============ COLLISION all at once ;D ================
# cm = N * Mraw * f_in
# # cm_eq = N*Mraw*feq
# # cm_after_collision = (eye(9)-S)*cm + S*cm_eq + (eye(9)-S/2.)*N*Mraw*body_force  # eq 8
# cm_after_collision = (eye(9)-S)*cm + S*cm_eq + (eye(9)-S/2.)*force_in_cm_space  # eq 8
#
# # back to densities space
# f_after_collision = Mraw.inv() * N.inv()*cm_after_collision
#
# print("\n\n=== PRETTY CODE all at once ;D ===\n\n")
# print_ccode(get_m00('f_in'), assign_to='real_t m00')
# print("")
# print_u2()
# print_as_vector_re(f_after_collision, "f_out")
#
# # print("\n\nby print_ccode \n")
# # for i in range(len(f_after_collision)):
# #     print_ccode(f_after_collision[i], assign_to='f_out[%s]' % i)






# // real_t F_i[9];
# // for ( int i=0; i < 9; i++){
# //         // F_i[i] = 3.0*wf[i] * (Fhydro.x*d2q9_ex[i] + Fhydro.y*d2q9_ey[i])/rho;
# //         F_i[i] = f_eq[i]*3.0*(Fhydro.x*(d2q9_ex[i]-u.x) + Fhydro.y*(d2q9_ey[i]-u.y))/rho;  // eq 11 - He et al. forcing scheme
# // }
