import numpy as np
from scipy import optimize
from joblib import Parallel, delayed
import multiprocessing
import time

class Similarity:
    # constants
    d = 0.000085  # free channel height

    kin_visc = 1.00E-06  # kinematic viscosity

    dyn_visc_ratio = 54.6  # dyn_visc_h/dyn_visc_l
    kin_visc_ratio = 6.67E-02  # kin_visc_h/kin_visc_l


    def __init__(self, Re=8.50E-01, We=1.17E-04, Ca=1.37E-04, Eo=1.10E-03):
        # similarity numbers to be matched
        self.Re_desired = Re
        self.We_desired = We
        self.Ca_desired = Ca
        self.Eo_desired = Eo

    def calc_sim_numbers(self, U, rho_h, Sigma, g):
        rho_ratio = Similarity.dyn_visc_ratio / Similarity.kin_visc_ratio  # rho_h/rho_l = 820 for water
        drho = rho_h - rho_h / rho_ratio
        mu = Similarity.kin_visc * rho_h

        Re = U * Similarity.d / Similarity.kin_visc
        Eo = drho * g * Similarity.d * Similarity.d / Sigma
        We = rho_h * U * U * Similarity.d / Sigma
        Ca = mu * U / Sigma
        return [Re, We, Ca, Eo]

    def calc_residua(self, U, rho_h, Sigma, g):
        [Re, We, Ca, Eo] = self.calc_sim_numbers(U, rho_h, Sigma, g)
        residua = [0.0001*(Re - self.Re_desired),
                   100*(We - self.We_desired),
                   100*(Ca - self.Ca_desired),
                   Eo - self.Eo_desired]
        return residua


# unknowns - initial guess
Umax0 = 0.01
rho_h0 = 1000
Sigma0 = 0.0728
g0 = 11.1

guess0 = [Umax0, rho_h0, Sigma0, g0]

# check residua at first step
def print_res_sim(U, rho_h, Sigma, g, similarity):
    print("\nResidua", similarity.calc_residua(U, rho_h, Sigma, g))
    [Re, We, Ca, Eo] = similarity.calc_sim_numbers(U, rho_h, Sigma, g)
    print("Similarity Numbers [Re = %10.2e , We = %10.2e , Ca = %10.2e,  Eo = %10.2e ]:" % (Re, We, Ca, Eo))


def check(guess, similarity):
    [Umax0, rho_h0, Sigma0, g0] = guess

    [Re, We, Ca, Eo] = similarity.calc_sim_numbers(Umax0, rho_h0, Sigma0, g0)
    similarity.calc_residua(Umax0, rho_h0, Sigma0, g0)
    print("GUESS0")
    print_res_sim(Umax0, rho_h0, Sigma0, g0, similarity)


def solve(guess, similarity):
    solution = optimize.root(lambda x, : similarity.calc_residua(x[0], x[1], x[2], x[3]),
                             guess, jac=None, tol=1e-6, method='lm')

    [U, rho_h, Sigma, g] = solution.x

    print("\nSOLUTION")
    print("U = %10.2e" % U)
    print('rho_h = %10.2e' % rho_h)
    print('Sigma = %10.2e' % Sigma)
    print('g = %10.2e' % g)

    print_res_sim(U, rho_h, Sigma, g, similarity)
    print("solution success status:", solution.success)


# sim = Similarity()
# check(guess0, sim)
# solve(guess0, sim)

print("\n\n ########### now calculate in lb world ############ \n\n")

Similarity.d = 85
Similarity.kin_visc = 0.5

dyn_visc_ratio = 54.6  # dyn_visc_h/dyn_visc_l
kin_visc_ratio = 1  # kin_visc_h/kin_visc_l

sim = Similarity(Re=0.1)

Umax0 = 5.88E-04
rho_h0 = 0.1
Sigma0 = 1.00E-02
g0 = 3.26E-07


guess0 = [Umax0, rho_h0, Sigma0, g0]

check(guess0, sim)
solve(guess0, sim)

print("\n\n ############## lb brute force search #####################")
search_range_ratio = 50
N = 5

vUmax = np.linspace(Umax0 / search_range_ratio, Umax0 * search_range_ratio, num=N)
vrho_h = np.linspace(rho_h0 / search_range_ratio, rho_h0 * search_range_ratio, num=N)
vSigma = np.linspace(Sigma0 / search_range_ratio, Sigma0 * search_range_ratio, num=N)
vg = np.linspace(g0 / search_range_ratio, g0 * search_range_ratio, num=N)


history = []

def check_solution(guess, similarity):
    solution = optimize.root(lambda x, : similarity.calc_residua(x[0], x[1], x[2], x[3]),
                             guess, jac=None, tol=1E-6, method='lm')

    [U, rho_h, Sigma, g] = solution.x

    if U < 0:
        return None

    if rho_h < 1E-3:
        return None

    if Sigma < 0 or Sigma > 0.1:
        return None

    if g < 0:
        return None

    return solution.x


start = time.time()
#
# for i in range(N):
#     for j in range(N):
#         for k in range(N):
#             for l in range(N):
#                 guess0 = [vUmax[i], vrho_h[j], vSigma[k], vg[l]]
#                 check_solution(guess0,sim)
#                 result = check_solution(guess0, sim)
#                 if result is not None:
#                     history.append(result)



def processInput(i):
    results = []
    for j in range(N):
        for k in range(N):
            for l in range(N):
                guess0 = [vUmax[i], vrho_h[j], vSigma[k], vg[l]]
                result = check_solution(guess0, sim)
                if result is not None:
                    results.append(result)
    return results


num_cores = multiprocessing.cpu_count()
history_list = Parallel(n_jobs=num_cores)(delayed(processInput)(i) for i in range(N))
history = sum(history_list, [])

end = time.time()
print("time [s]: ", end - start)

print("U \t rho_h \t Sigma \t g")
for i in range(len(history)):
    [U, rho_h, Sigma, g] = history[i]
    [Re, We, Ca, Eo] = sim.calc_sim_numbers(U, rho_h, Sigma, g)
    print("[U = %10.3e, rho_h = %10.3e, Sigma = %10.3e, g = %10.3e ] \t"
          "[Re = %10.1e, We = %10.1e, Ca = %10.1e, Eo = %10.1e ]:"
          % (U, rho_h, Sigma, g, Re, We, Ca, Eo))

