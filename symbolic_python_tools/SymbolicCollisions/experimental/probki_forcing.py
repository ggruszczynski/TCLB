from SymbolicCollisions.core.sym_col_fun import *
from SymbolicCollisions.core.printers import print_as_vector, print_ccode
import numpy as np
import time
from sympy.utilities.iterables import flatten
from sympy import pretty_print
from sympy import *
start = time.process_time()

print('// === welcome to cm! === \n ')
print('// === discrete cm ===\n ')


# print('\n//F_cm_Guo_extended')
# F_cm_Guo_extended = get_cm_vector_from_discrete_def(get_force_Guo_second_order)
# print_as_vector(F_cm_Guo_extended, 'F_cm', regex=True)
#
#
# print('\n//N*M*F_cm_Guo_extended ')
# F_cm_Guo_extended = get_cm_vector_shift_NM(get_force_Guo_second_order)
# print_as_vector(F_cm_Guo_extended, 'F_cm', regex=True)

print('\n\n// === continous cm === \n ')


# print('\n//Force -> Force_cm - from continous definition: \n'
#       'k_mn = integrate(fun, (x, -oo, oo), (y, -oo, oo)) \n'
#       'where fun = forceM(rho,u,x,y) *(x-ux)^m (y-uy)^n ')
# F_cm = get_cm_vector_from_continuous_def(get_continuous_force_Guo_second_order)
# print_as_vector(F_cm, 'F_cm', regex=True)

# print('\n//population_eq -> cm_eq - from continous definition: \n'
#       'k_mn = integrate(fun, (x, -oo, oo), (y, -oo, oo)) \n'
#       'where fun = fM(rho,u,x,y) *(x-ux)^m (y-uy)^n')
# # cm_eq = get_cm_vector_from_continuous_def(get_continuous_Maxwellian_DF)
# cm_eq = get_cm_vector_from_continuous_def(get_continuous_hydro_DF)
# print_as_vector(cm_eq, 'cm_eq', regex=True)

print('\n//Force -> Force_cm - from continous definition: \n'
      'k_mn = integrate(fun, (x, -oo, oo), (y, -oo, oo)) \n'
      'where fun = forceM(rho,u,x,y) *(x-ux)^m (y-uy)^n ')
# F_cm = get_cm_vector_from_continuous_def(get_continuous_force_He_first_order_MB)
F_cm = get_cm_vector_from_continuous_def(get_continuous_force_He_hydro_DF)
print_as_vector(F_cm, 'F_cm', regex=True)


print('\n\n Done in %s [s].'
      % str(time.process_time() - start))
