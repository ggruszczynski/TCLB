"""
See 1.60, 1.61 p34
PhD Thesis `Lattice Boltzmann Simulation of Multiphase Flows;
Application to Wave Breaking and Sea Spray Generation`
by Amir Banari 2014
"""


class TwoPhasePoiseuilleAnal:
    def __init__(self, u_c, mu_l, mu_g, rho_l, rho_g, h):
        self.u_c = u_c  # velocity at the center
        self.mu_g = mu_g  # dynamic viscosity of gas
        self.mu_l = mu_l  # dynamic viscosity of liquid
        self.rho_g = rho_g  # density of gas
        self.rho_l = rho_l  # density of liquid

        self.h = h  # distance from the center to the channel walls

        self.gx = u_c * (mu_l + mu_g) / (h * h)  # body force

    def get_u_profile(self, y):
        if y > 0:
            result = -self.rho_g * (y / self.h) * (y / self.h)
            result -= (y / self.h) * (self.mu_g * self.rho_l - self.mu_l * self.rho_g) / (self.mu_l + self.mu_g)
            result += (self.rho_g + self.rho_l) * self.mu_g / (self.mu_l + self.mu_g)

            result *= self.gx * self.h * self.h / (2 * self.mu_g)

            return result
        else:
            result = -self.rho_l*(y / self.h) * (y / self.h)
            result -= (y / self.h) * (self.mu_g * self.rho_l - self.mu_l * self.rho_g) / (self.mu_l + self.mu_g)
            result += + (self.rho_g + self.rho_l) * self.mu_l / (self.mu_l + self.mu_g)

            result *= self.gx * self.h * self.h / (2 * self.mu_l)
            return result

    def get_uc_from_gx(self, gx=None):

        if gx is None:
            gx = self.gx

        uc = gx * self.h * self.h / (self.mu_l + self.mu_g)
        return uc

