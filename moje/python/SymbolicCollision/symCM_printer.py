

from SymbolicCollision.sym_col_utils import *
import time
start = time.process_time()
print('// === welcome to cm! === \n ')
print('// === discrete cm ===\n ')

print('\n//F_cm_He_original')
F_cm_He_original = get_cm_vector_from_discrete_def(get_force_He_original)
print_as_vector_re(F_cm_He_original, 'F_cm')

# print('\n//N*M*F_He_original ')
# NMF_cm_He_original = get_cm_vector_shift_NM(get_force_He_original)
# print_as_vector_re(NMF_cm_He_original, 'F_cm')
#
# print('\n//F_cm_He_pf')
# F_cm_He_pf = get_cm_vector_from_discrete_def(get_force_He_pf)
# print_as_vector_re(F_cm_He_pf, 'F_cm')
#
#
# print('\n//F_cm_Guo_bez_U')
# F_cm_Guo_bez_U = get_cm_vector_from_discrete_def(get_force_Guo_bez_U)
# print_as_vector_re(F_cm_Guo_bez_U, 'F_cm')
#
# print('\n//F_cm_Guo')
# F_cm_Guo = get_cm_vector_from_discrete_def(get_force_Guo_first_order)
# print_as_vector_re(F_cm_Guo, 'F_cm')
#
# print('\n//F_cm_Guo_extended')
# F_cm_Guo_extended = get_cm_vector_from_discrete_def(get_force_Guo_second_order)
# print_as_vector_re(F_cm_Guo_extended, 'F_cm')
#
# print('\n//F_phi_cm')
# F_phi_cm = get_cm_vector_from_discrete_def(get_force_interface_tracking)
# print_as_vector_re(F_phi_cm, 'F_phi_cm')
#
#
# print('\n//population_eq -> cm_eq - by definition: k_mn = sum( (e_ix-ux)^m (e_iy-uy)^n * population_eq_i)')
# pop_eq = get_cm_vector_from_discrete_def(lambda i: Symbol('m00') * get_gamma(i))
# print_as_vector_re(pop_eq, 'pop_eq')
#
# print('\n//population -> cm - by definition: k_mn = sum( (e_ix-ux)^m (e_iy-uy)^n * population_i)')
# pop_cm = get_cm_vector_from_discrete_def(lambda i: Symbol('%s[%d]' % ('pop', i)))
# print_as_vector_re(pop_cm, 'pop_cm')
#
# print('\n//phase-field hydrodynamic model: population_eq_pf -> cm_eq_pf - by definition: '
#       '\n//k_mn = sum( (e_ix-ux)^m (e_iy-uy)^n * population_eq_pf_i)')
# cm_eq_pf = get_cm_vector_from_discrete_def(get_pop_eq_pf)
# print_as_vector_re(cm_eq_pf, 'cm_eq_pf')

print('\n\n// === continous cm === \n ')
print('\n//population_eq -> cm_eq - from continous definition: \n'
      'k_mn = integrate(fun, (dzeta_x, -oo, oo), (dzeta_y, -oo, oo)) \n'
      'where fun = fM(rho,u,x,y) *(x-ux)^m (y-uy)^n')

cm_eq = get_cm_vector_from_continous_def(get_continous_Maxwellian_DF)
print_as_vector_re(cm_eq, 'cm_eq')

print('\n//Force -> Force_cm - from continous definition: \n'
      'k_mn = integrate(fun, (dzeta_x, -oo, oo), (dzeta_y, -oo, oo)) \n'
      'where fun = forceM(rho,u,x,y) *(x-ux)^m (y-uy)^n ')

F_cm = get_cm_vector_from_continous_def(get_continous_force_He_original)
print_as_vector_re(F_cm, 'F_cm')

print('\n\n Done in %s [s]!'
      % str(time.process_time() - start))
