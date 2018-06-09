

from SymbolicCollisions.core.sym_col_fun import *
from SymbolicCollisions.core.printers import print_as_vector, print_ccode

import time
start = time.process_time()

print('// === welcome to cm! === \n ')
print('// === discrete cm ===\n ')

print('\n//F_cm_He_first_order')
F_cm_He_original = get_cm_vector_from_discrete_def(get_force_He_first_order)
# F_cm_He_original = get_cm_vector_from_discrete_def(get_force_He_second_order)  # produces looong expressions
print_as_vector(F_cm_He_original, 'F_cm', regex=True)

print('\n//N*M*F_He_first_order')
NMF_cm_He_original = get_cm_vector_shift_NM(get_force_He_first_order)
print_as_vector(NMF_cm_He_original, 'F_cm', regex=True)

print('\n//F_cm_He_hydro_eq_experimental')
F_cm_He_pf = get_cm_vector_from_discrete_def(get_force_He_hydro_eq_experimental)
print_as_vector(F_cm_He_pf, 'F_cm', regex=True)


print('\n//F_cm_Guo_without_U')
F_cm_Guo_bez_U = get_cm_vector_from_discrete_def(get_force_Guo_without_U_experimental)
print_as_vector(F_cm_Guo_bez_U, 'F_cm', regex=True)

print('\n//F_cm_Guo')
F_cm_Guo = get_cm_vector_from_discrete_def(get_force_Guo_first_order)
print_as_vector(F_cm_Guo, 'F_cm', regex=True)

print('\n//F_cm_Guo_extended')
F_cm_Guo_extended = get_cm_vector_from_discrete_def(get_force_Guo_second_order)
print_as_vector(F_cm_Guo_extended, 'F_cm', regex=True)

print('\n//F_phi_cm')
F_phi_cm = get_cm_vector_from_discrete_def(get_force_interface_tracking)
print_as_vector(F_phi_cm, 'F_phi_cm', regex=True)


print('\n//population_eq -> cm_eq - by definition: k_mn = sum( (e_ix-ux)^m (e_iy-uy)^n * population_eq_i)')
pop_eq = get_cm_vector_from_discrete_def(lambda i: Symbol('m00') * get_gamma(i))
print_as_vector(pop_eq, 'pop_eq', regex=True)

print('\n//population -> cm - by definition: k_mn = sum( (e_ix-ux)^m (e_iy-uy)^n * population_i)')
pop_cm = get_cm_vector_from_discrete_def(lambda i: Symbol('%s[%d]' % ('pop', i)))
print_as_vector(pop_cm, 'pop_cm', regex=True)

print('\n//phase-field hydrodynamic model: population_eq_pf -> cm_eq_pf - by definition: '
      '\n//k_mn = sum( (e_ix-ux)^m (e_iy-uy)^n * population_eq_pf_i)')
cm_eq_pf = get_cm_vector_from_discrete_def(get_pop_eq_hydro)
print_as_vector(cm_eq_pf, 'cm_eq_pf', regex=True)


print('\n\n// === continous cm === \n ')

print('\n//population_eq -> cm_eq - from continous definition: \n'
      'k_mn = integrate(fun, (x, -oo, oo), (y, -oo, oo)) \n'
      'where fun = fM(rho,u,x,y) *(x-ux)^m (y-uy)^n')
cm_eq = get_cm_vector_from_continuous_def(get_continuous_Maxwellian_DF)
# cm_eq = get_cm_vector_from_continuous_def(get_continuous_hydro_DF)
print_as_vector(cm_eq, 'cm_eq', regex=True)

print('\n//Force -> Force_cm - from continous definition: \n'
      'k_mn = integrate(fun, (x, -oo, oo), (y, -oo, oo)) \n'
      'where fun = forceM(rho,u,x,y) *(x-ux)^m (y-uy)^n ')
F_cm = get_cm_vector_from_continuous_def(get_continuous_force_He_first_order_MB)
# F_cm = get_cm_vector_from_continuous_def(get_continuous_force_He_hydro_DF)
print_as_vector(F_cm, 'F_cm', regex=True)

print('\n//Force -> Force_cm - from continous definition: \n'
      'k_mn = integrate(fun, (x, -oo, oo), (y, -oo, oo)) \n'
      'where fun = forceM(rho,u,x,y) *(x-ux)^m (y-uy)^n ')
F_cm = get_cm_vector_from_continuous_def(get_continuous_force_Guo_second_order)
print_as_vector(F_cm, 'F_cm', regex=True)

print('\n//N*M*F_He_continous ')
NMF_cm_He_original = get_cm_vector_shift_NM(get_continuous_force_He_first_order_MB)
print_as_vector(NMF_cm_He_original, 'F_cm', regex=True)  # produces looong expressions


print('\n\n Done in %s [s].'
      % str(time.process_time() - start))

