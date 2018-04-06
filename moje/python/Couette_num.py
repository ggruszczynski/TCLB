import matplotlib.pyplot as plt
import numpy as np

u_lid = 0.0001

H = 98
h = 46


def u_bottom(y, mi_h, mi_l):
    u_m = h * mi_h * u_lid / (H * mi_l - h * mi_l + h * mi_h)
    ans = y * u_m / h
    return ans


def u_top(y, mi_h, mi_l):
    u_m = h * mi_h * u_lid / (H * mi_l - h * mi_l + h * mi_h)
    ans = u_m + (y-h)*(u_lid-u_m)/(H - h)
    return ans


def u_Couette_anal(y, mi_h, mi_l):
    if y < h:
        return u_bottom(y, mi_h, mi_l)
    else:
        return u_top(y, mi_h, mi_l)


# x = np.linspace(0, H, 1000)
# y = [u_Couette_anal(x[i]) for i in range(len(x))]


# plt.figure()
# plt.plot(x, y, "b-")
#
# plt.grid(True)
# plt.xlabel("h")
# plt.ylabel("u")
#
# plt.title("u(h)")
#
# plt.show()

