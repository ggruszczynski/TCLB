from sympy import Symbol
from sympy.interactive.printing import init_printing
from sympy.matrices import Matrix, eye, zeros, ones, diag, GramSchmidt
from sympy import exp, pi, integrate, oo
from sympy import simplify, Float, preorder_traversal


init_printing(use_unicode=False, wrap_line=False, no_global=True)

# SYMBOLS:
ux = Symbol('u.x')
uy = Symbol('u.y')

sv = Symbol('s_v')  # s_v = 1 /(tau + 0.5)
sb = Symbol('s_b')  # results in bulk viscosity = 1/6 since : zeta = (1/sb - 0.5)*cs^2*dt

ex = Matrix([0, 1, 0, -1, 0, 1, -1, -1, 1])
ey = Matrix([0, 0, 1, 0, -1, 1, 1, -1, -1])

Fx = Symbol('Fhydro.x')
Fy = Symbol('Fhydro.y')

F_phi_x = Symbol('F_phi.x')
F_phi_y = Symbol('F_phi.y')

phi_norm_grad_x = Symbol('norm_grad_phi.x')  # normalized gradient of the phase field in the x direction
phi_norm_grad_y = Symbol('norm_grad_phi.y')  # normalized gradient of the phase field in the y direction
F_phi_coeff = Symbol('F_phi_coeff')  # F_phi_coeff=(1.0 - 4.0*(myPhaseF - pfavg)*(myPhaseF - pfavg))/inteface_width;

m00 = Symbol('m00')
rho = Symbol('rho')
w = Matrix([4. / 9, 1. / 9, 1. / 9, 1. / 9, 1. / 9, 1. / 36, 1. / 36, 1. / 36, 1. / 36])

uxuy = Symbol('uxuy')
ux2 = Symbol('ux2')
uy2 = Symbol('uy2')

ux3 = Symbol('ux3')
uy3 = Symbol('uy3')
uxuy3 = Symbol('uxuy3')

dzeta_x = Symbol('dzeta_x')
dzeta_y = Symbol('dzeta_y')



# this matrix will produce raw moments (m=M*f) in the following order:
# [m00, m10, m01, m20, m02, m11, m21, m12, m22]
# "Modelling incompresiible thermal flows using a central-moments-based lattice Boltzmann method" L. Fei et al. 2017
Mraw = Matrix([
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, -1, 0, 1, -1, -1, 1],
    [0, 0, 1, 0, -1, 1, 1, -1, -1],
    [0, 1, 0, 1, 0, 1, 1, 1, 1],
    [0, 0, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, -1, 1, -1],
    [0, 0, 0, 0, 0, 1, 1, -1, -1],
    [0, 0, 0, 0, 0, 1, -1, -1, 1],
    [0, 0, 0, 0, 0, 1, 1, 1, 1]
])


# eq 10.30 from The Lattice Boltzmann Method: Principles and Practice
# T. Krüger, H. Kusumaatmaja, A. Kuzmin, O. Shardt, G. Silva, E.M. Viggen
M_ortho_GS = Matrix([
    [ 1,  1,  1,  1,  1, 1,  1,  1,  1],
    [-4, -1, -1, -1, -1, 2,  2,  2,  2],
    [ 4, -2, -2, -2, -2, 1,  1,  1,  1],
    [ 0,  1,  0, -1,  0, 1, -1, -1,  1],
    [ 0, -2,  0,  2,  0, 1, -1, -1,  1],
    [ 0,  0,  1,  0, -1, 1,  1, -1, -1],
    [ 0,  0, -2,  0,  2, 1,  1, -1, -1],
    [ 0,  1, -1,  1, -1, 0,  0,  0,  0],
    [ 0,  0,  0,  0,  0, 1, -1,  1, -1]
])


ex_Straka_d2_q5 = Matrix([0, -1, 0, 1, 0])
ey_Straka_d2_q5 = Matrix([0, 0, -1, 0, 1])

K_ortho_Straka_d2q5 = Matrix([  # in Geier's lattice numbering CSYS
    [1,  0,  0,  4,  0],  # 0
    [1, -1,  0, -1, -1],  # 1
    [1,  0, -1, -1,  1],  # 2
    [1,  1,  0, -1, -1],  # 3
    [1,  0,  1, -1,  1],  # 4
])

Shift_ortho_Straka_d2q5 = Matrix([  # in Geier's lattice numbering CSYS
    [2,  0, 0, 0],  # 1
    [0,  2, 0, 0],  # 2
    [-4 * ux,  0,  -2, -2],  # 3
    [0,  -4 * uy,  -2,  2],  # 4
])

ex_Geier = Matrix([0, -1, -1, -1, 0, 1, 1, 1, 0])
ey_Geier = Matrix([0, 1, 0, -1, -1, -1, 0, 1, 1])

K_ortho_Geier = Matrix([  # in Geier's lattice numbering CSYS
    [1,  0,  0, -4,  0,  0,  0,  0,  4],  # 0
    [1, -1,  1,  2,  0,  1, -1,  1,  1],  # 1
    [1, -1,  0, -1,  1,  0,  0, -2, -2],  # 2
    [1, -1, -1,  2,  0, -1,  1,  1,  1],  # 3
    [1,  0, -1, -1, -1,  0, -2,  0, -2],  # 4
    [1,  1, -1,  2,  0,  1,  1, -1,  1],  # 5
    [1,  1,  0, -1,  1,  0,  0,  2, -2],  # 6
    [1,  1,  1,  2,  0, -1, -1, -1,  1],  # 7
    [1,  0,  1, -1, -1,  0,  2,  0, -2],  # 8
])

Shift_ortho_Geier = Matrix([
    [6, 2, 0, 0, 0, 0],   # noqa
    [6, -2, 0, 0, 0, 0],   # noqa
    [0, 0, -4, 0, 0, 0],   # noqa
    [            -6 * uy,         -2 * uy,        8 * ux,     -4,      0, 0],  # noqa
    [            -6 * ux,          2 * ux,        8 * uy,      0,     -4, 0],  # noqa
    [8 + 6 * (ux2 + uy2), 2 * (uy2 - ux2), -16 * ux * uy, 8 * uy, 8 * ux, 4],
])

# raw moments - interpretation
# real_t m00 = f[0] + f[1] + f[2] + f[3] + f[4] + f[5] + f[6] + f[7]  + f[8];  // m00 - m0: density
# real_t m10 =        f[1]        - f[3]        + f[5] - f[6] - f[7]  + f[8];  // m10 - m1: x momentum flux
# real_t m01 =             + f[2]        - f[4] + f[5] + f[6] - f[7]  - f[8];  // m01 - m2: y momentum flux
# real_t m20 =        f[1]        + f[3]        + f[5] + f[6] + f[7]  + f[8];  // m20 - m3
# real_t m02 =               f[2]        + f[4] + f[5] + f[6] + f[7]  + f[8];  // m02 - m4
# real_t m11 =                                    f[5] - f[6] + f[7]  - f[8];  // m11 - m5: stress tensor xy (off-diagonal)
# real_t m21 =                                    f[5] + f[6] - f[7]  - f[8];  // m21 - m6
# real_t m12 =                                    f[5] + f[6] - f[7]  - f[8];  // m12 - m7
# real_t m22 =                                    f[5] + f[6] + f[7]  + f[8];  // m22 - m8

# SHIFT MATRIX
# "Modelling incompresiible thermal flows using a central-moments-based lattice Boltzmann method" L. Fei et al. 2017
N = Matrix([
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [-ux, 1, 0, 0, 0, 0, 0, 0, 0],
    [-uy, 0, 1, 0, 0, 0, 0, 0, 0],
    [ux * ux, -2 * ux, 0, 1, 0, 0, 0, 0, 0],
    [uy * uy, 0, -2 * uy, 0, 1, 0, 0, 0, 0],
    [ux * uy, -uy, -ux, 0, 0, 1, 0, 0, 0],
    [-ux * ux * uy, 2 * ux * uy, ux * ux, -uy, 0, -2 * ux, 1, 0, 0],
    [-uy * uy * ux, uy * uy, 2 * ux * uy, 0, -ux, -2 * uy, 0, 1, 0],
    [ux * ux * uy * uy, -2 * ux * uy * uy, -2 * uy * ux * ux, uy * uy, ux * ux, 4 * ux * uy, -2 * uy, -2 * ux, 1],
])

# RELAXATION MATRIX
s_plus = (sb + sv) / 2
s_minus = (sb - sv) / 2

S_relax = diag(1, 1, 1, s_plus, s_plus, sv, 1, 1, 1)
S_relax[3, 4] = s_minus
S_relax[4, 3] = s_minus

S_relax_MRT_GS = diag(1, 1, 1, 1, 1, 1, 1, sv, sv)   #
# S_relax_MRT_GS = diag(0, 0, 0, 0, 0, 0, 0, sv, sv)   #

# save time and hardcode F_cm
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
