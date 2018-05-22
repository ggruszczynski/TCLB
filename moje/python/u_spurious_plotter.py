import matplotlib.pyplot as plt
import csv
import numpy as np
import os
from utilites import remove_duplicates_y



def read_data(filename):
    x = np.empty(0)
    u = np.empty(0)

    with open(os.path.join("data_for_plots", "relaxation_interpolation", filename), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        headers = next(reader, None)  # returns the headers or `None` if the input is empty

        for row in reader:
            x = np.append(x, float(row[0]))
            u = np.append(u, float(row[1]))

    x, u = remove_duplicates_y(x, u)
    return x, u


x23, u_eq23_rho10 = read_data("mrt_u_spurious_eq_23.csv")
x25, u_eq25_rho10 = read_data("mrt_u_spurious_eq_25.csv")


# make plot
plt.rcParams.update({'font.size': 24})
plt.figure(figsize=(12, 8))
# plt.plot(rho_ratio, u_MRT_Guo, color="red", marker=".", linestyle="", label='u MRT linear relaxation')
plt.semilogy(x23 / x23.max(), u_eq23_rho10.flatten(), color="green", label=r'$ eq23$')
plt.semilogy(x25 / x25.max(), u_eq25_rho10.flatten(), color="red", label=r'$ eq25$')

plt.xlabel(r'$x$')
plt.ylabel(r'$u$')

plt.title('Spurious currents')
plt.grid(True)
plt.legend()

rho_ratio = '100'
plt.text(0.0, 5E-6, r'$\rho^* = %s$' % rho_ratio)
fig = plt.gcf()  # get current figure
fig.savefig('spurious_currents_MRTrho%s.png' % rho_ratio)
plt.show()
