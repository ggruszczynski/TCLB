import re
from SymbolicCollision.utils.cm_symbols import ux, uy, uxuy, ux2, uy2, ux3, uy3, uxuy3
from sympy.printing import print_ccode

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
