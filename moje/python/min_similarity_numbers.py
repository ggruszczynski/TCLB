import numpy as np
from scipy import optimize

class Similarity:
    # constants
    d = 100  # free channel height
    rho_ratio = 1  # rho_h/rho_l
    kin_visc = 0.02987  # kinematic viscosity


    def __init__(self, Re=1.09E-0, We=1.674E-04, Eo=1.363E-03):

        # similarity numbers to be matched
        self.Re_desired = Re
        self.We_desired = We
        self.Eo_desired = Eo

    def calc_sim_numbers(self, U, Sigma, g):
        # drho = rho_h - rho_h / Similarity.rho_ratio

        rho_h = 1
        drho = 1

        Re = U * Similarity.d / Similarity.kin_visc
        We = rho_h * U * U * Similarity.d / Sigma
        Eo = drho * g * Similarity.d * Similarity.d / Sigma


        return [Re, We, Eo]

    def calc_residua(self, U, Sigma, g):
        [Re, We, Eo] = self.calc_sim_numbers(U, Sigma, g)
        residua = [Re - self.Re_desired,
                   We - self.We_desired,
                   Eo - self.Eo_desired]
        return residua

    def calc_residua_wrapper(self, x):
        # wrapper is required to match scipy.optimize.root
        res = np.array(self.calc_residua(x[0], x[1], x[2]))
        norm = np.linalg.norm(res.reshape((3, 1)), ord='fro')
        return norm


import numpy as np
from scipy import optimize




# unknowns - initial guess
U0 = 3.272e-4
Sigma0 = 6.42e-2
g0 = 8.72e-9

# U0 = 0.00025389499999999997
# Sigma0 = 0.0550963000167945
# g0 = 6.060593001723061e-09

guess = np.array([U0, Sigma0, g0])

# check residua at first step
similarity = Similarity()
[Re, We, Eo] = similarity.calc_sim_numbers(U0, Sigma0, g0)

print("Residua step0: ", similarity.calc_residua(U0, Sigma0, g0))




from scipy.optimize import rosen, rosen_der
from scipy.optimize import minimize
# method='Powell' - same result as optimize.root(similarity.calc_residua_wrapper, guess, jac=None, tol=1e-5, method='hybr')

# solution = minimize(similarity.calc_residua_wrapper, guess, method='BFGS', jac=rosen_der,
#                options={'gtol': 1e-12, 'disp': True})

solution = minimize(similarity.calc_residua_wrapper, guess, method="Nelder-Mead")


[U, Sigma, g] = solution.x

print("U = %10.2e" % U)
# print('rho_h = %10.2e' % rho_h)
print('Sigma = %10.2e' % Sigma)
print('g = %10.2e' % g)
print("\n Residua - solved:", similarity.calc_residua(U, Sigma, g))
print("\n Similarity Numbers [Re, We, Eo]:", similarity.calc_sim_numbers(U, Sigma, g))
print(solution.message)


print("\n ========================= another method ===================================")
# And variables must be positive, hence the following bounds:
bnds = ((0, None), (0, None), (0, None))
cons = ({'type': 'ineq', 'fun': lambda x: x[0] - 1e-10},  # U
        {'type': 'ineq', 'fun': lambda x: x[1] - 1e-10},  # Sigma
        {'type': 'ineq', 'fun': lambda x: x[2] - 1e-10},)  # g
# minimize f(x) subject to
# g_i(x) >= 0,  i = 1,...,m
# h_j(x)  = 0,  j = 1,...,p

solution = minimize(similarity.calc_residua_wrapper, guess,
            method='SLSQP',
            bounds=bnds,
            constraints=cons,
            tol=1e-9)

[U, Sigma, g] = solution.x
print("U = %10.2e" % U)
# print('rho_h = %10.2e' % rho_h)
print('Sigma = %10.2e' % Sigma)
print('g = %10.2e' % g)

print("\n Residua - solved:", similarity.calc_residua(U, Sigma, g))
[Re, We, Eo] = similarity.calc_sim_numbers(U, Sigma, g)
print("\n Similarity Numbers [Re = %10.2e , We = %10.2e , Eo = %10.2e ]:" % (Re, We, Eo))
print(solution.message)