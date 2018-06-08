
from sympy.matrices import Matrix
from SymbolicCollisions.core.cm_symbols import m00, rho, \
    Fx, Fy, F_phi_x, F_phi_y, \
    ux, uy, ux2, uy2, uxuy


# save time and hardcode some of the results
hardcoded_F_cm_hydro_LB_density_based = Matrix([
    0,
    Fx * m00 / rho,
    Fy * m00 / rho,
    0,
    0,
    0,
    Fy * m00 / (rho * 3.),
    Fx * m00 / (rho * 3.),
    0,
])

hardcoded_F_cm_hydro_LB_velocity_based = Matrix([
    0,
    Fx / rho,
    Fy / rho,
    0,
    0,
    0,
    Fy / (rho * 3.),
    Fx / (rho * 3.),
    0,
])

hardcoded_F_cm_pf = Matrix([
    0,
    F_phi_x,
    F_phi_y,
    0,
    0,
    0,
    F_phi_y / 3.,
    F_phi_x / 3.,
    0,
])


# save time and hardcode cm_eq_pf - eq10
hardcoded_cm_pf_eq = Matrix([m00,
                             0,
                             0,
                             m00 / 3.,
                             m00 / 3.,
                             0,
                             0,
                             0,
                             m00 / 9.,
                             ])


# save time and hardcode cm_eq_pf - eq16
hardcoded_cm_hydro_eq = Matrix([
    m00,
    ux * (-m00 + 1),
    uy * (-m00 + 1),
    m00 * ux2 + 1. / 3. * m00 - ux2,
    m00 * uy2 + 1. / 3. * m00 - uy2,
    uxuy * (m00 - 1),
    uy * (-m00 * ux2 - 1. / 3. * m00 + ux2 + 1. / 3.),
    ux * (-m00 * uy2 - 1. / 3. * m00 + uy2 + 1. / 3.),
    m00 * ux2 * uy2 + 1. / 3. * m00 * ux2 + 1. / 3. * m00 * uy2 + 1. / 9. * m00 - ux2 * uy2 - 1. / 3. * ux2 - 1. / 3. * uy2,
    ])
