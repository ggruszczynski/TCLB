"""
M - distributions to raw moment transformation matrix
N - raw moments to central moments transformation matrix

based on:
'Modeling incompressible thermal flows using a central-moment-based lattice Boltzmann method'
Linlin Fei, Kai Hong Luo, Chuandong Lin, Qing Li
2017
"""

from SymbolicCollision.cm_symbols import *
from sympy import simplify, Float, preorder_traversal
import re


init_printing(use_unicode=False, wrap_line=False, no_global=True)


# HELPERS:
def print_u2():
    print("real_t %s = %s*%s;" % (uxuy, ux, uy))
    print("real_t %s = %s*%s;" % (ux2, ux, ux))
    print("real_t %s = %s*%s;" % (uy2, uy, uy))
    print("")


def print_u3():
    print("real_t %s = %s*%s;" % (ux3, ux2, ux))
    print("real_t %s = %s*%s;" % (uy3, uy2, uy))
    print("real_t %s = %s*%s*%s;" % (uxuy3, uxuy, uxuy, uxuy))
    print("")


def print_as_vector_re(some_matrix, print_symbol='default_symbol1'):
    rows = some_matrix._mat

    for i in range(len(rows)):
        row = str(rows[i])
        row = re.sub("%s\*\*2" % ux, '%s' % ux2, row)
        row = re.sub("%s\*\*2" % uy, '%s' % uy2, row)
        row = re.sub("%s\*%s" % (ux, uy), '%s' % uxuy, row)

        row = re.sub("%s\*\*3" % ux, '%s' % ux3, row)
        row = re.sub("%s\*\*3" % uy, '%s' % uy3, row)
        row = re.sub("%s\*\*3" % uxuy, '%s' % uxuy3, row)

        row = re.sub("0.333333333333333", "1./3.", row)
        row = re.sub("0.33333333333333", "1./3.", row)
        row = re.sub("0.111111111111111", "1./9.", row)
        row = re.sub("0.11111111111111", "1./9.", row)
        row = re.sub("0.22222222222222", "2./9.", row)
        row = re.sub("0.166666666666667", "1./6.", row)
        row = re.sub("0.66666666666667", "2./3.", row)
        row = re.sub("1.0\*", "", row)
        print("%s[%d] = %s;" % (print_symbol, i, row))

        # raw
        # print("%s[%d] = %s;" % (print_symbol, i, rows[i]))


def print_as_vector_raw(some_matrix, print_symbol='default_symbol1'):
    rows = some_matrix._mat

    for i in range(len(rows)):
        row = str(rows[i])
        print("%s[%d] = %s;" % (print_symbol, i, row))


def get_populations(print_symbol='default_symbol2'):
    symbols_ = [Symbol("%s[%d]" % (print_symbol, i)) for i in range(9)]

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


def get_force_He_original(i):
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


def get_force_He_pf(i):
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


def get_force_Guo_bez_U(i):
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
    # cs2 = Symbol('cs2')
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
    # cs2 = Symbol('cs2')
    dzeta_2 = dzeta_x_*dzeta_x_ + dzeta_y_*dzeta_y_
    dzeta_u2 = (dzeta_x_ - ux) * (dzeta_x_ - ux) + (dzeta_y_ - uy) * (dzeta_y_ - uy)

    # DF_p = 0
    DF_p = (m00-1) / (2 * pi * cs2)*exp(-dzeta_2 / (2 * cs2))

    # DF_p = (m00) / (2 * pi * cs2)*exp(-dzeta_2 / (2 * cs2))
    # DF_p = -1/(2 * pi * cs2)*exp(-dzeta_2 / (2 * cs2))

    # DF_gamma = 0
    DF_gamma = 1 / (2 * pi * cs2)*exp(-dzeta_u2 / (2 * cs2))

    return DF_p + DF_gamma


def get_continuous_force_He_original(dzeta_x_=dzeta_x, dzeta_y_=dzeta_x, DF=get_continuous_Maxwellian_DF):
    """
    'Discrete Boltzmann equation model for the incompressible Navier-Stokes equation', He et al., 1998
    """
    cs2 = 1. / 3.
    # cs2 = Symbol('cs2')
    euF = (dzeta_x_ - ux) * Fx + (dzeta_y_ - uy) * Fy
    R = DF(dzeta_x_, dzeta_y_) * euF / (rho * cs2)
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
