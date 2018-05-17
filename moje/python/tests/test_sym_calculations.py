import numpy as np
from numpy.testing import assert_almost_equal
from unittest import TestCase

import io
from contextlib import redirect_stdout
from sympy import Symbol

from SymbolicCollision.sym_col_utils import get_cm_eq_vector, get_pop_eq_pf, get_force_He_original, get_gamma
from SymbolicCollision.sym_col_utils import print_as_vector_re


class TestSymbolicCalc(TestCase):

    def test_get_force_He_original(self):
        F_in_cm = get_cm_eq_vector(get_force_He_original)

        f = io.StringIO()
        with redirect_stdout(f):
            print_as_vector_re(F_in_cm, 'F_in_cm')
        out = f.getvalue()

        expected_result = 'F_in_cm[0] = 0;\n' \
                          'F_in_cm[1] = Fhydro.x*m00/rho;\n' \
                          'F_in_cm[2] = Fhydro.y*m00/rho;\n' \
                          'F_in_cm[3] = -3.0*m00*ux2*(Fhydro.x*u.x + Fhydro.y*u.y)/rho;\n' \
                          'F_in_cm[4] = -3.0*m00*uy2*(Fhydro.x*u.x + Fhydro.y*u.y)/rho;\n' \
                          'F_in_cm[5] = -3.0*m00*uxuy*(Fhydro.x*u.x + Fhydro.y*u.y)/rho;\n' \
                          'F_in_cm[6] = m00*(9.0*Fhydro.x*ux3*u.y + 9.0*Fhydro.y*ux2*uy2 + 1./3.*Fhydro.y)/rho;\n' \
                          'F_in_cm[7] = m00*(9.0*Fhydro.x*ux2*uy2 + 1./3.*Fhydro.x + 9.0*Fhydro.y*uxuy3)/rho;\n' \
                          'F_in_cm[8] = -m00*(18.0*Fhydro.x*ux3*uy2 + Fhydro.x*ux3 + 3.0*Fhydro.x*u.x*uy2 + 18.0*Fhydro.y*ux2*uy3 + 3.0*Fhydro.y*ux2*u.y + Fhydro.y*uy3)/rho;\n'  # noqa

        assert 'F_in_cm[0] = 0;' in out
        assert 'F_in_cm[1] = Fhydro.x*m00/rho;' in out
        assert 'F_in_cm[2] = Fhydro.y*m00/rho;' in out
        assert 'F_in_cm[3] = -3.0*m00*ux2*(Fhydro.x*u.x + Fhydro.y*u.y)/rho;\n' in out
        assert 'F_in_cm[4] = -3.0*m00*uy2*(Fhydro.x*u.x + Fhydro.y*u.y)/rho;\n' in out
        assert 'F_in_cm[5] = -3.0*m00*uxuy*(Fhydro.x*u.x + Fhydro.y*u.y)/rho;\n' in out
        assert 'F_in_cm[6] = m00*(9.0*Fhydro.x*ux3*u.y + 9.0*Fhydro.y*ux2*uy2 + 1./3.*Fhydro.y)/rho;\n' in out
        assert 'F_in_cm[7] = m00*(9.0*Fhydro.x*ux2*uy2 + 1./3.*Fhydro.x + 9.0*Fhydro.y*uxuy3)/rho;\n' in out
        assert 'F_in_cm[8] = -m00*(18.0*Fhydro.x*ux3*uy2 + Fhydro.x*ux3 + 3.0*Fhydro.x*u.x*uy2 + 18.0*Fhydro.y*ux2*uy3 + 3.0*Fhydro.y*ux2*u.y + Fhydro.y*uy3)/rho;\n' in out  # noqa

        assert expected_result == out

    def test_get_pop_eq(self):
        cm_eq = get_cm_eq_vector(get_pop_eq_pf)

        f = io.StringIO()
        with redirect_stdout(f):
            print_as_vector_re(cm_eq, 'cm_eq')
        out = f.getvalue()

        expected_result = 'cm_eq[0] = m00;\n' \
                          'cm_eq[1] = u.x*(-m00 + 1);\n' \
                          'cm_eq[2] = u.y*(-m00 + 1);\n' \
                          'cm_eq[3] = m00*ux2 + 1./3.*m00 - ux2;\n' \
                          'cm_eq[4] = m00*uy2 + 1./3.*m00 - uy2;\n' \
                          'cm_eq[5] = uxuy*(m00 - 1);\n' \
                          'cm_eq[6] = u.y*(-m00*ux2 - 1./3.*m00 + 1./3.);\n' \
                          'cm_eq[7] = u.x*(-m00*uy2 - 1./3.*m00 + 1./3.);\n' \
                          'cm_eq[8] = m00*ux2*uy2 + 1./3.*m00*ux2 + 1./3.*m00*uy2 + 1./9.*m00 + 2.0*ux2*uy2 - 1./3.*ux2 - 1./3.*uy2;\n'  # noqa

        assert 'cm_eq[0] = m00;' in out
        assert 'cm_eq[2] = u.y*(-m00 + 1)' in out
        assert 'cm_eq[2] = u.y*(-m00 + 1);' in out
        assert 'cm_eq[3] = m00*ux2 + 1./3.*m00 - ux2;\n' in out
        assert 'cm_eq[4] = m00*uy2 + 1./3.*m00 - uy2;\n' in out
        assert 'cm_eq[5] = uxuy*(m00 - 1);\n' in out
        assert 'cm_eq[6] = u.y*(-m00*ux2 - 1./3.*m00 + 1./3.);\n' in out
        assert 'cm_eq[7] = u.x*(-m00*uy2 - 1./3.*m00 + 1./3.);\n' in out
        assert 'cm_eq[8] = m00*ux2*uy2 + 1./3.*m00*ux2 + 1./3.*m00*uy2 + 1./9.*m00 + 2.0*ux2*uy2 - 1./3.*ux2 - 1./3.*uy2;\n' in out  # noqa

        assert expected_result == out

    def test_cm_eq(self):
        """
        test eq 10 from
        'Modeling incompressible thermal flows using a central-moment-based lattice Boltzmann method'
        Linlin Fei, Kai Hong Luo, Chuandong Lin, Qing Li
        2017
        """

        cm_eq = get_cm_eq_vector(lambda i: Symbol('m00') * get_gamma(i))

        f = io.StringIO()
        with redirect_stdout(f):
            print_as_vector_re(cm_eq, 'cm_eq')
        out = f.getvalue()

        expected_result = 'cm_eq[0] = m00;\n' \
                          'cm_eq[1] = 0;\n' \
                          'cm_eq[2] = 0;\n' \
                          'cm_eq[3] = 1./3.*m00;\n' \
                          'cm_eq[4] = 1./3.*m00;\n' \
                          'cm_eq[5] = 0;\n' \
                          'cm_eq[6] = -m00*ux2*u.y;\n' \
                          'cm_eq[7] = -m00*u.x*uy2;\n' \
                          'cm_eq[8] = m00*(3.0*ux2*uy2 + 1./9.);\n'  # noqa

        assert 'cm_eq[0] = m00;' in out
        assert 'cm_eq[2] = 0;' in out
        assert 'cm_eq[2] = 0;' in out
        assert 'cm_eq[3] = 1./3.*m00;\n' in out
        assert 'cm_eq[4] = 1./3.*m00;\n' in out
        assert 'cm_eq[5] = 0;\n' in out
        assert 'cm_eq[6] = -m00*ux2*u.y;\n' in out
        assert 'cm_eq[7] = -m00*u.x*uy2;\n' in out
        assert 'cm_eq[8] = m00*(3.0*ux2*uy2 + 1./9.);\n' in out  # noqa

        assert expected_result == out
