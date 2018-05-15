import numpy as np
from scipy import optimize
from joblib import Parallel, delayed
import multiprocessing
import time

from utilites import remove_duplicates


class Similarity:
    def __init__(self, sim_num, d=85, kin_visc_h=0.1):
        # similarity numbers to be matched
        self.simNumDesired = sim_num
        self.d = d  # free channel height
        self.kin_visc_h = kin_visc_h

    def calc_sim_numbers(self, U, rho_h, sigma):

        dyn_visc_h = self.kin_visc_h*rho_h

        Re = U * self.d / self.kin_visc_h
        We = rho_h * U * U * self.d / sigma
        Ca = dyn_visc_h * U / sigma
        return [Re, We, Ca]

    def calc_residua(self, U, rho_h, sigma):
        (Re, We, Ca) = self.calc_sim_numbers(U, rho_h, sigma)
        residua = [0.1 * (Re - self.simNumDesired["Re"]),
                   1 * (We - self.simNumDesired["We"]),
                   1 * (Ca - self.simNumDesired["Ca"])]
        return residua


# check residua at first step
def print_res_sim(U, rho_h, sigma, similarity):
    print("\nResidua", similarity.calc_residua(U, rho_h, sigma))
    [Re, We, Ca] = similarity.calc_sim_numbers(U, rho_h, sigma)
    print("Similarity Numbers [Re = %10.2e , We = %10.2e , Ca = %10.2e ]:" % (Re, We, Ca))


def check(guess, similarity):
    [Umax0, rho_h0, Sigma0] = guess

    [Re, We, Ca] = similarity.calc_sim_numbers(Umax0, rho_h0, Sigma0)
    similarity.calc_residua(Umax0, rho_h0, Sigma0)
    print("GUESS0")
    print_res_sim(Umax0, rho_h0, Sigma0, similarity)


def solve(guess, similarity):
    solution = optimize.root(lambda x,: similarity.calc_residua(x[0], x[1], x[2]),
                             guess, jac=None, tol=1e-6, method='lm')

    [U, rho_h, Sigma] = solution.x

    print("\nSOLUTION")
    print("U = %10.2e" % U)
    print('rho_h = %10.2e' % rho_h)
    print('Sigma = %10.2e' % Sigma)

    gravity = U * 8 * similarity.kin_visc_h / (similarity.d * similarity.d)

    print('g = %10.2e' % gravity)
    print_res_sim(U, rho_h, Sigma, similarity)
    print("solution success status:", solution.success)


print("\n\n ########### now calculate in lb world ############ \n\n")

SimNum = {"Re": 8.5E-01, "We": 1.17E-04, "Ca": 1.37E-04}
sim = Similarity(SimNum, d=850, kin_visc_h=0.5)

Umax0 = 1.0E-04
rho_h0 = 1.0E-01
Sigma0 = 1.00E-02

guess0 = [Umax0, rho_h0, Sigma0]

check(guess0, sim)
solve(guess0, sim)

print("\n\n ############## lb brute force search #####################")
search_range_ratio = 10
N = 10

vUmax = np.linspace(Umax0 / search_range_ratio, Umax0 * search_range_ratio, num=N)
vrho_h = np.linspace(rho_h0 / search_range_ratio, rho_h0 * search_range_ratio, num=N)
vSigma = np.linspace(Sigma0 / search_range_ratio, Sigma0 * search_range_ratio, num=N)


def check_solution(guess, similarity):
    solution = optimize.root(lambda x,: similarity.calc_residua(x[0], x[1], x[2]),
                             guess, jac=None, tol=1E-6, method='lm')

    (U, rho_h, Sigma) = solution.x

    if U < 0:
        return None

    if rho_h < 1E-02:
        return None

    if Sigma < 0 or Sigma > 0.1:
        return None

    return solution.x


start = time.time()


# for i in range(N):
#     for j in range(N):
#         for k in range(N):
#             for l in range(N):
#                 guess0 = [vUmax[i], vrho_h[j], vSigma[k]]
#                 check_solution(guess0,sim)
#                 result = check_solution(guess0, sim)
#                 if result is not None:
#                     history_list.append(result)


def process_input(i):
    results = []
    for j in range(N):
        for k in range(N):
            for l in range(N):
                guess_0 = [vUmax[i], vrho_h[j], vSigma[k]]
                result = check_solution(guess_0, sim)
                if result is not None:
                    results.append(result)
    return results


num_cores = multiprocessing.cpu_count()
history_list = Parallel(n_jobs=num_cores)(delayed(process_input)(i) for i in range(N))
history = sum(history_list, [])

end = time.time()
print("time [s]: ", end - start)

history = remove_duplicates(history)
history.sort(key=lambda x: x[1], reverse=True)  # U, rho, sigma

print("=== U \t rho_h \t Sigma ===")
for i in range(len(history)):
    [U, rho_h, Sigma] = history[i]
    [Re, We, Ca] = sim.calc_sim_numbers(U, rho_h, Sigma)

    g = U * 8 * sim.kin_visc_h / (sim.d * sim.d)

    print("[U = %10.3e, rho_h = %10.3e, Sigma = %10.3e, kin_visc = %10.2e, g = %10.2e] \t"
          "[Re = %10.1e, We = %10.1e, Ca = %10.1e]:"
          % (U, rho_h, Sigma, sim.kin_visc_h, g, Re, We, Ca))


# solve(guess=[8.376e-05, 1.194e-01, 1.606e-04], similarity=sim)
