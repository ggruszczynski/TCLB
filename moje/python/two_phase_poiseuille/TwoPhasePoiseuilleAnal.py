"""
See eq36
`Phase-field-based lattice Boltzmann modelling of large-density-ratio two-phase flows`
by H. Liang, J. Xu, H. Wang, Z Chai, B. Shi, 2018
"""


class TwoPhasePoiseuilleAnal:
    def __init__(self, u_c, mu_l, mu_g, h):
        self.u_c = u_c   # velocity at the center
        self.mu_g = mu_g  # dynamic viscosity of gas
        self.mu_l = mu_l  # dynamic viscosity of liquid
        self.h = h  # distance from the center to the channel walls

        self.gx = u_c * (mu_l + mu_g) / (h * h)  # body force

    def get_u_profile(self, y):
        if y > 0:
            result = -(y / self.h) * (y / self.h) - \
                     (y / self.h) * (self.mu_g - self.mu_l)/(self.mu_l + self.mu_g) \
                     + 2 * self.mu_g / (self.mu_l + self.mu_g)

            result *= self.gx * self.h * self.h / (2 * self.mu_g)

            return result

        else:
            result = -(y / self.h) * (y / self.h) - \
                     (y / self.h) * (self.mu_g - self.mu_l)/(self.mu_l + self.mu_g) \
                     + 2 * self.mu_l / (self.mu_l + self.mu_g)

            result *= self.gx * self.h * self.h / (2 * self.mu_l)
            return result
