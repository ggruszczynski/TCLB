"""
M - distributions to raw moment transformation matrix
N - raw moments to central moments transformation matrix

based on:
'Modeling incompressible thermal flows using a central-moment-based lattice Boltzmann method'
Linlin Fei, Kai Hong Luo, Chuandong Lin, Qing Li
2017
"""

from sympy import exp, pi, integrate, oo
from sympy import Symbol
from sympy.matrices import Matrix
from sympy.interactive.printing import init_printing
from SymbolicCollisions.core.cm_symbols import ex, ey, ux, uy, ux, w, m00, \
    Fx, Fy, F_phi_x, F_phi_y, rho, dzeta_x, dzeta_y, \
    N, Mraw
from sympy import simplify, Float, preorder_traversal


init_printing(use_unicode=False, wrap_line=False, no_global=True)


def get_populations(print_symbol='default_symbol2', start=0, end=9):
    symbols_ = [Symbol("%s[%d]" % (print_symbol, i)) for i in range(start, end)]

    return Matrix(symbols_)


def get_m00(print_symbol='default_symbol3'):
    m00_ = Symbol("%s[%d]" % (print_symbol, 0))

    for i in range(1, 9):
        m00_ += Symbol("%s[%d]" % (print_symbol, i))

    return m00_


def get_e():
    symbols_ = [Matrix([ex[i], ey[i]]) for i in range(9)]
    return Matrix([symbols_])


def get_gamma(i):
    cs2 = 1. / 3.
    # cs2 = Symbol('cs2')
    eu = ex[i] * ux + ey[i] * uy
    u2 = ux * ux + uy * uy
    gamma = w[i] * (1 + eu / cs2 + eu * eu / (2 * cs2 * cs2) - u2 / (2 * cs2))
    return gamma


def get_pop_eq_hydro(i):
    gamma = get_gamma(i)
    g = m00 * w[i] + gamma - w[i]
    return g


def get_force_He_first_order(i):
    """
    'Discrete Boltzmann equation model for the incompressible Navier-Stokes equation', He et al., 1998
    """
    cs2 = 1. / 3.
    # cs2 = Symbol('cs2')
    euF = (ex[i] - ux) * Fx + (ey[i] - uy) * Fy
    pop_eq = m00 * get_gamma(i)
    R = pop_eq * euF / (rho * cs2)
    return R


def get_force_He_second_order(i):
    # extended version with second order terms
    cs2 = 1. / 3.
    temp_x = ex[i] - ux + (ex[i] * ux + ey[i] * uy) * ex[i] / cs2
    temp_y = ey[i] - uy + (ex[i] * ux + ey[i] * uy) * ey[i] / cs2
    pop_eq = m00 * get_gamma(i)
    R = pop_eq * (temp_x * Fx + temp_y * Fy) / (rho * cs2)
    return R


def get_force_He_hydro_eq_experimental(i):
    """
    'Discrete Boltzmann equation model for the incompressible Navier-Stokes equation', He et al., 1998
    version for 'Improved locality of the phase-field lattice-Boltzmann model for immiscible fluids at high density ratios' A. Fakhari et. al., 2017
    """
    cs2 = 1. / 3.
    # cs2 = Symbol('cs2')
    euF = (ex[i] - ux) * Fx + (ey[i] - uy) * Fy
    pop_eq = get_pop_eq_hydro(i)
    # R = pop_eq*euF/(p_star*cs2)
    R = pop_eq * euF / (rho * cs2)
    return R


def get_force_Guo_without_U_experimental(i):
    """
    'Discrete lattice effects on the forcing term in the lattice Boltzmann method',  Guo et al., 2001
    version for 'Improved locality of the phase-field lattice-Boltzmann model for immiscible fluids at high density ratios' A. Fakhari et. al., 2017
    """
    # first order terms only
    cs2 = 1. / 3.
    # # cs2 = Symbol('cs2')
    # eF = (ex[i] - ux) * Fx + (ey[i] - uy) * Fy  # TODO why (ey[i] - uy)
    eF = ex[i] * Fx + ey[i] * Fy
    R = w[i] * eF / (rho * cs2)
    return R


def get_force_Guo_first_order(i):
    """
    'Discrete lattice effects on the forcing term in the lattice Boltzmann method',  Guo et al., 2001
    version for 'Improved locality of the phase-field lattice-Boltzmann model for immiscible fluids at high density ratios' A. Fakhari et. al., 2017
    """
    # first order terms only
    cs2 = 1. / 3.
    # # cs2 = Symbol('cs2')
    eF = (ex[i] - ux) * Fx + (ey[i] - uy) * Fy  # TODO why (ey[i] - uy)
    # eF = ex[i]*Fx + ey[i]*Fy
    R = w[i] * eF / (rho * cs2)
    return R


def get_force_Guo_second_order(i):
    """
    'Discrete lattice effects on the forcing term in the lattice Boltzmann method',  Guo et al., 2001
    version for 'Improved locality of the phase-field lattice-Boltzmann model for immiscible fluids at high density ratios' A. Fakhari et. al., 2017
    """
    # extended version with second order terms
    cs2 = 1. / 3.
    temp_x = ex[i] - ux + (ex[i] * ux + ey[i] * uy) * ex[i] / cs2
    temp_y = ey[i] - uy + (ex[i] * ux + ey[i] * uy) * ey[i] / cs2
    R = w[i] * (temp_x * Fx + temp_y * Fy) / (rho * cs2)
    return R


def get_force_interface_tracking(i):
    """
    'Improved locality of the phase-field lattice-Boltzmann model for immiscible fluids at high density ratios' A. Fakhari et. al., 2017
    eq7 in cm
    """
    # R = F_phi_coeff * w[i]*(ex[i]*phi_norm_grad_x + ey[i]*phi_norm_grad_y)  #improve results a bit

    # try Guo:
    # extended version with second order terms
    cs2 = 1. / 3.
    temp_x = ex[i] - ux + (ex[i] * ux + ey[i] * uy) * ex[i] / cs2
    temp_y = ey[i] - uy + (ex[i] * ux + ey[i] * uy) * ey[i] / cs2
    R = w[i] * (temp_x * F_phi_x + temp_y * F_phi_y) / cs2
    return R


def round_and_simplify(stuff):
    simplified_stuff = simplify(stuff)
    rounded_stuff = simplified_stuff

    for a in preorder_traversal(simplified_stuff):
        if isinstance(a, Float):
            rounded_stuff = rounded_stuff.subs(a, round(a, 14))

    rounded_and_simplified_stuff = simplify(rounded_stuff)
    return rounded_and_simplified_stuff


def get_discrete_m(m, n, fun):
    k = 0
    for i in range(9):
        # pop = get_pop_eq(i)
        # pop = p_star * get_gamma(i)
        # pop = Symbol('f[%d]' % i)
        pop = fun(i)
        k += pow(ex[i], m) * pow(ey[i], n) * pop

    return round_and_simplify(k)


def get_discrete_cm(m, n, fun):
    k = 0
    for i in range(9):
        # pop = get_pop_eq(i)
        # pop = p_star * get_gamma(i)
        # pop = Symbol('f[%d]' % i)
        pop = fun(i)
        k += pow((ex[i] - ux), m) * pow((ey[i] - uy), n) * pop

    return round_and_simplify(k)


def get_cm_vector_from_discrete_def(fun):
    cm_ = [get_discrete_cm(0, 0, fun),
           get_discrete_cm(1, 0, fun),
           get_discrete_cm(0, 1, fun),
           get_discrete_cm(2, 0, fun),
           get_discrete_cm(0, 2, fun),
           get_discrete_cm(1, 1, fun),
           get_discrete_cm(2, 1, fun),
           get_discrete_cm(1, 2, fun),
           get_discrete_cm(2, 2, fun)
           ]
    return Matrix([cm_])


def get_cm_vector_shift_NM(fun):
    pop = Matrix([fun(i) for i in range(9)])
    # pop = Matrix(9, 1, lambda i,j: i+j)  # column vect
    cm_ = N * Mraw * pop
    cm_ = round_and_simplify(cm_)
    return Matrix([cm_])


def get_continuous_Maxwellian_DF(dzeta_x_=dzeta_x, dzeta_y_=dzeta_x):
    """
    :param dzeta: direction (x,y)
    :param u: velocity (x,y)
    :param rho: density
    :return: continous, local Maxwell-Boltzmann distribution
    'Incorporating forcing terms in cascaded lattice Boltzmann approach by method of central moments'
    Kannan N. Premnath, Sanjoy Banerjee, 2009
    eq 22
    """
    cs2 = 1. / 3.
    dzeta_u2 = (dzeta_x_ - ux) * (dzeta_x_ - ux) + (dzeta_y_ - uy) * (dzeta_y_ - uy)
    DF = m00 / (2 * pi * cs2)
    DF *= exp(-dzeta_u2 / (2 * cs2))

    return DF

def get_continuous_hydro_DF(dzeta_x_=dzeta_x, dzeta_y_=dzeta_x):
    """
    :param dzeta: direction (x,y)
    :param u: velocity (x,y)
    :param rho: density
    :return: continous, local Maxwell-Boltzmann distribution
    """
    cs2 = 1. / 3.
    dzeta_2 = dzeta_x_*dzeta_x_ + dzeta_y_*dzeta_y_
    DF_p = (m00-1) / (2 * pi * cs2)*exp(-dzeta_2 / (2 * cs2))

    dzeta_u2 = (dzeta_x_ - ux) * (dzeta_x_ - ux) + (dzeta_y_ - uy) * (dzeta_y_ - uy)
    DF_gamma = 1 / (2 * pi * cs2)*exp(-dzeta_u2 / (2 * cs2))

    return DF_p + DF_gamma


def get_continuous_force_He_hydro_DF(dzeta_x_=dzeta_x, dzeta_y_=dzeta_x):
    """
    'Discrete Boltzmann equation model for the incompressible Navier-Stokes equation', He et al., 1998
    """
    cs2 = 1. / 3.
    euF = (dzeta_x_ - ux) * Fx + (dzeta_y_ - uy) * Fy
    R = get_continuous_hydro_DF(dzeta_x_, dzeta_y_) * euF / (rho * cs2)
    return R


def get_continuous_force_He_second_order_MB(dzeta_x_=dzeta_x, dzeta_y_=dzeta_x):
    cs2 = 1. / 3.
    # cs2 = Symbol('cs2')

    cs2 = 1. / 3.
    temp_x = dzeta_x_ - ux + (dzeta_x_ * ux + dzeta_y_ * uy) * dzeta_x_ / cs2
    temp_y = dzeta_y_ - uy + (dzeta_x_ * ux + dzeta_y_ * uy) * dzeta_y_ / cs2

    euF2 = (temp_x * Fx + temp_y * Fy)/cs2  # second order
    R = get_continuous_Maxwellian_DF(dzeta_x_, dzeta_y_) * euF2 / (rho * cs2)
    return R


def get_continuous_force_He_first_order_MB(dzeta_x_=dzeta_x, dzeta_y_=dzeta_x):
    """
    'Discrete Boltzmann equation model for the incompressible Navier-Stokes equation', He et al., 1998
    Use Maxwellian to calculate equilibria
    """
    cs2 = 1. / 3.
    # cs2 = Symbol('cs2')
    euF = (dzeta_x_ - ux) * Fx + (dzeta_y_ - uy) * Fy
    R = get_continuous_Maxwellian_DF(dzeta_x_, dzeta_y_) * euF / (rho * cs2)
    return R


def get_continous_cm(m, n, DF):
    fun = DF(dzeta_x, dzeta_y) * pow((dzeta_x - ux), m) * pow((dzeta_y - uy), n)

    result = integrate(fun, (dzeta_x, -oo, oo), (dzeta_y, -oo, oo))
    return round_and_simplify(result)


def get_cm_vector_from_continuous_def(fun):
    cm_ = [get_continous_cm(0, 0, fun),
           get_continous_cm(1, 0, fun),
           get_continous_cm(0, 1, fun),
           get_continous_cm(2, 0, fun),
           get_continous_cm(0, 2, fun),
           get_continous_cm(1, 1, fun),
           get_continous_cm(2, 1, fun),
           get_continous_cm(1, 2, fun),
           get_continous_cm(2, 2, fun)
           ]
    return Matrix([cm_])
