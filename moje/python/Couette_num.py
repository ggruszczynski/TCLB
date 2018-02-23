import matplotlib.pyplot as plt
import numpy as np

u_lid = 0.0001

mi_t = 0.166
mi_b = 0.0166
H = 98
h = 49
u_m = h * mi_t * u_lid / (H * mi_b - h * mi_b + h * mi_t)
print(u_m)

# def um(h):
#     # ans = h*u_t*mi_t /(H*mi_b - h*(mi_b + mi_t))
#     ans = h * mi_t * u_t / (H * mi_b - h * mi_b + h * mi_t)
#     return ans
#     # return np.sin(h)



def u_bottom(y):
    ans = y * u_m / h
    return ans


def u_top(y):
    ans = y * (u_lid - u_m)/(H-h) + u_m - h*(u_lid - u_m)/(H - h)
    return ans


def u(y):
    if y < h:
        return u_bottom(y)
    else:
        return u_top(y)


x = np.linspace(0, H, 1000)

y = [u(x[i]) for i in range(len(x))]


plt.figure()

# plt.plot(x, y, "b.")
plt.plot(x, y, "b-")

plt.grid(True)
plt.xlabel("h")
plt.ylabel("u")

plt.title("u(h)")

plt.show()
