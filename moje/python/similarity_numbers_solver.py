import numpy as np
from scipy import optimize




guess = np.zeros((1, 2), float)



def fun(x):
    return [x[0] + 0.5 * (x[0] - x[1]) ** 3 - 1.0,
            0.5 * (x[1] - x[0]) ** 3 + x[1]]


def jac(x):
    return np.array([[1 + 1.5 * (x[0] - x[1])**2,
                      -1.5 * (x[0] - x[1])**2],
                     [-1.5 * (x[1] - x[0])**2,
                      1 + 1.5 * (x[1] - x[0])**2]])


sol = optimize.root(fun, guess, jac=jac, method='hybr')
sol.x
print(sol.x)


def fun2_wrapper(x):
    a = x[0]
    b = x[1]

    def fun2(x0, x1):
        residua = [x0 + 0.5 * (x0 - x1) ** 3 - 1,
                   0.5 * (x1 - x0) ** 3 + x1]

        return residua

    return fun2(a, b)


sol2 = optimize.root(fun2_wrapper, guess, jac=None, method='hybr')
sol2.x

print(sol2.x)


class MyClass:
    def __init__(self, var=1):
        self.var = var


    def wrapper (self, x):
        a = x[0]
        b = x[1]

        def method(x0, x1):
            residua = [x0 + 0.5 * (x0 - x1) ** 3 - self.var,
                      0.5 * (x1 - x0) ** 3 + x1]

            return residua

        return method(a, b)


myClass = MyClass()

sol3 = optimize.root(myClass.wrapper, guess, jac=None, method='hybr')
sol3.x

print(sol3.x)







class Similarity:
    # constants
    d = 0.000085  # free channel height
    rho_ratio = 820  # rho_h/rho_l
    kin_visc = 1.00E-06  # kinematic viscosity

    def __init__(self, Re=8.50E-01, We=1.17E-04, Ca=1.37E-04, Eo=1.10E-03):

        # similarity numbers to be matched
        self.Re_desired = Re
        self.We_desired = We
        self.Ca_desired = Ca
        self.Eo_desired = Eo

    def calc_sim_numbers(self, U, rho_h, Sigma, g):
        drho = rho_h - rho_h / Similarity.rho_ratio
        mu = Similarity.kin_visc * rho_h

        Re = U * Similarity.d / Similarity.kin_visc
        Eo = drho * g * Similarity.d * Similarity.d / Sigma
        We = rho_h * U * U * Similarity.d / Sigma
        Ca = mu * U / Sigma

        return [Re, We, Ca, Eo]

    def calc_residua(self, U, rho_h, Sigma, g):
        [Re, We, Ca, Eo] = self.calc_sim_numbers(U, rho_h, Sigma, g)
        residua = [Re - self.Re_desired,
                   We - self.We_desired,
                   Ca - self.Ca_desired,
                   Eo - self.Eo_desired]
        return residua

    def calc_residua_wrapper(self, x):
        # wrapper is required to match scipy.optimize.root API
        return self.calc_residua(x[0], x[1], x[2], x[3])


# unknowns - initial guess
U0 = 0.01
rho_h0 = 1000
Sigma0 = 0.0728
g0 = 11.1

guess = [U0, rho_h0, Sigma0, g0]

# check residua at first step
similarity = Similarity()
[Re, We, Ca, Eo] = similarity.calc_sim_numbers(U0, rho_h0, Sigma0, g0)
similarity.calc_residua(U0, rho_h0, Sigma0, g0)
print("Residua step0: ", similarity.calc_residua(U0, rho_h0, Sigma0, g0))

# solve
solution = optimize.root(similarity.calc_residua_wrapper, guess, jac=None, tol=1e-5, method='hybr')
[U, rho_h, Sigma, g] = solution.x


print("U = %10.2e" % U)
print('rho_h = %10.2e' % rho_h)
print('Sigma = %10.2e' % Sigma)
print('g = %10.2e' % g)

print("Residua - solved:", similarity.calc_residua_wrapper([U, rho_h, Sigma, g]))

asdfds = 123

