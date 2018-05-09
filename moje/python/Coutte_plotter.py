import matplotlib.pyplot as plt
import csv
import numpy as np
import os
from Couette_num import u_Couette_anal
from utilites import clip_x, normalize, remove_duplicates_y


def read_data(filename):
    x = np.empty(0)
    u = np.empty(0)

    with open(os.path.join("data_for_plots", "Couette", filename), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        headers = next(reader, None)  # returns the headers or `None` if the input is empty

        for row in reader:
            x = np.append(x, float(row[0]))
            u = np.append(u, float(row[1]))

    x, u = remove_duplicates_y(x, u)
    return x, u


x_rho, u_rho = read_data("uCouette_2phase_rho*10.csv")
x_v, u_v = read_data("uCouette_2phase_v*10.csv")


# x_rho, u_rho = read_data("uCouette_2phase_rho*100.csv")
# x_v, u_v = read_data("uCouette_2phase_v*100.csv")

x_anal = np.linspace(0, 100, num=99)
u_anal = [u_Couette_anal(x_anal[i], mi_h=1.0, mi_l=0.1) for i in range(len(x_anal))]

# u_anal_54 = [u_Couette_anal(x_anal[i], mi_h=0.166, mi_l=0.00304029304) for i in range(len(x_anal))]
# u_anal_10 = [u_Couette_anal(x_anal[i], mi_h=1.0, mi_l=0.1) for i in range(len(x_anal))]
# u_anal_100 = [u_Couette_anal(x_anal[i], mi_h=1.0, mi_l=0.01) for i in range(len(x_anal))]
# u_anal_1000 = [u_Couette_anal(x_anal[i], mi_h=1.0, mi_l=0.001) for i in range(len(x_anal))]

# make plot
plt.rcParams.update({'font.size': 28})
plt.figure(figsize=(12, 8))
# plt.plot(x_anal/len(x_anal), u_anal_1000/max(u_anal_1000), color="blue",  linestyle="--", label=r'$\mu^* = 1000$')
# plt.plot(x_anal/len(x_anal), u_anal_54/max(u_anal_54), color="red", label=r'$\mu^* = 54.6$')
# plt.plot(x_anal/len(x_anal), u_anal_10/max(u_anal_10), color="green", linestyle="--", label=r'$\mu^* = 10$')


plt.plot(x_rho/max(x_rho), u_anal/max(u_anal), color="red", label=r'$u_{analytical}$')
plt.plot(x_rho/max(x_rho), u_rho/max(u_anal), color="green", linestyle="--", label=r'$rho^* = 10$')
plt.plot(x_v/max(x_v), u_v/max(u_anal), color="blue",  linestyle="--", label=r'$v^* = 10$')


# plt.plot(x, u1/u_avg, color="blue", marker="", linestyle="--", label="through the centre of air water interface")
plt.xlabel(r'$x/D$')
plt.ylabel(r'$u/U_{max}$')

# plt.title('Velocity profile \n two phase Couette flow')

plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
fig.savefig('Couette_benchmark_10.png')
# fig.savefig('Couette_benchmark_slip_validation.png')
plt.show()