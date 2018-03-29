import numpy as np
from scipy import optimize
from joblib import Parallel, delayed
import multiprocessing
import time


class Similarity:
    def __init__(self, sim_num, d=85, kin_visc_h=0.1, rho_h=1.0):
        # similarity numbers to be matched
        self.simNumDesired = sim_num
        self.d = d  # free channel height
        self.kin_visc_h = kin_visc_h
        self.rho_h = rho_h

    def calc_sim_numbers(self, U,  sigma):

        dyn_visc_h = self.kin_visc_h*self.rho_h

        Re = U * self.d / self.kin_visc_h
        Ca = dyn_visc_h * U / sigma

        return [Re, Ca]

    def calc_residua(self, U, sigma):
        (Re, Ca) = self.calc_sim_numbers(U,  sigma)
        residua = [0.1 * (Re - self.simNumDesired["Re"]),
                   1 * (Ca - self.simNumDesired["Ca"])]
        return residua


# check residua at first step
def print_res_sim(U, sigma, similarity):
    print("\nResidua", similarity.calc_residua(U, sigma))
    [Re, Ca] = similarity.calc_sim_numbers(U, sigma)
    print("Similarity Numbers [Re = %10.2e , Ca = %10.2e ]:" % (Re, Ca))


def check(guess, similarity):
    [Umax0, Sigma0] = guess

    [Re, Ca] = similarity.calc_sim_numbers(Umax0, Sigma0)
    similarity.calc_residua(Umax0, Sigma0)
    print("GUESS0")
    print_res_sim(Umax0, Sigma0, similarity)


def solve(guess, similarity):
    solution = optimize.root(lambda x,: similarity.calc_residua(x[0], x[1]),
                             guess, jac=None, tol=1e-6, method='lm')

    [U, Sigma] = solution.x

    print("\nSOLUTION")
    print("U = %10.2e" % U)
    print('rho_h = %10.2e' % similarity.rho_h)
    print('Sigma = %10.2e' % Sigma)

    gravity = U * 8 * similarity.kin_visc_h / (similarity.d * similarity.d)

    print('g = %10.2e' % gravity)
    print_res_sim(U, Sigma, similarity)
    print("solution success status:", solution.success)


print("\n\n ########### now calculate in lb world ############ \n\n")

# SimNum = {"Re": 8.5E-01, "Ca": 1.37E-04}
SimNum = {"Re": 1.0E-01, "Ca": 1.0E-02}
sim = Similarity(SimNum, d=425, kin_visc_h=0.5, rho_h=1)

Umax0 = 1.0E-04
Sigma0 = 1.00E-04

guess0 = [Umax0, Sigma0]

check(guess0, sim)
solve(guess0, sim)

print("\n\n ############## lb brute force search #####################")
search_range_ratio = 100
N = 10

vUmax = np.linspace(Umax0 / search_range_ratio, Umax0 * search_range_ratio, num=N)
vSigma = np.linspace(Sigma0 / search_range_ratio, Sigma0 * search_range_ratio, num=N)


def check_solution(guess, similarity):
    solution = optimize.root(lambda x,: similarity.calc_residua(x[0], x[1]),
                             guess, jac=None, tol=1E-6, method='lm')

    (U, Sigma) = solution.x

    if U < 0:
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
    for k in range(N):
        for l in range(N):
            guess_0 = [vUmax[i], vSigma[k]]
            result = check_solution(guess_0, sim)
            if result is not None:
                results.append(result)
    return results


num_cores = multiprocessing.cpu_count()
history_list = Parallel(n_jobs=num_cores)(delayed(process_input)(i) for i in range(N))
history = sum(history_list, [])

end = time.time()
print("time [s]: ", end - start)


def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        h = hash(tuple(value))  # convert to tuple, list are un-hashable since they can change order
        if h not in seen:
            output.append(value)
            seen.add(h)
    return output


history = remove_duplicates(history)
history.sort(key=lambda x: x[1], reverse=True)  # U, rho, sigma

print("=== U \t rho_h \t Sigma ===")
for i in range(len(history)):
    [U, Sigma] = history[i]
    [Re, Ca] = sim.calc_sim_numbers(U, Sigma)

    g = U * 8 * sim.kin_visc_h / (sim.d * sim.d)
    We = sim.rho_h * U * U * sim.d / Sigma

    print("[U = %10.3e, Sigma = %10.3e, g = %10.2e] \t"
          "[Re = %10.1e, Ca = %10.2e,  We = %10.2e]:"
          % (U, Sigma, g, Re, Ca, We))


# solve(guess=[8.376e-05, 1.194e-01, 1.606e-04], similarity=sim)
