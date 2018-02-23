import matplotlib.pyplot as plt
import numpy as np


mi = 0.166
dp = 0.001

H = 128  # channel height
R = H / 2
L = 256  # channel length


def dp_to_u_max():
    u_max = R * R * dp / (2 * mi * L)
    return u_max


def u_max_to_dp(u_max):
    dp = u_max * (2 * mi * L)/(R*R)
    return dp


def u_dp(y):
    """
    :return: velocity profile given pressure difference
    """

    u = - y *(y - H) * dp / (2 * mi * L)
    return u

u_max = dp_to_u_max()

def u_inlet(y, umax, R):
    """
    :return: velocity profile based on channel height and u_max
    :parameter: u_max - in the middle of the pipe
    It has to match the pressure-inlet pressure-outlet profile
    """

    u = umax * (2 * y * R - y*y)/(R*R)
    return u

x = np.linspace(0, H, 500)

y_dp = [u_dp(x[i]) for i in range(len(x))]
y_inlet = [u_inlet(x[i], u_max, R) for i in range(len(x))]


# plt.figure()
#
# plt.plot(x, y_dp, color="red", marker=".", linestyle="", label="pressure driven")
# plt.plot(x, y_inlet, color="blue", marker="", linestyle="--", label="velocity inlet")
#
# plt.grid(True)
# plt.xlabel("h")
# plt.ylabel("u")
# plt.legend()
#
# plt.title("u_dp(h) and u_inlet(h) ")
#
# plt.show()
