import matplotlib.pyplot as plt
import csv
import numpy as np
import os
from utilites import remove_duplicates_y



rho_ratio = [1, 10, 100, 1000]
u_MRT_Guo = [6.00E-08, 1.10E-07, 1.30E-07, 1.30E-07]

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


x, u_lin10 = read_data("u_spurious_MRT_lin_rho10.csv")

# make plot
plt.figure(figsize=(12, 8))
# plt.plot(rho_ratio, u_MRT_Guo, color="red", marker=".", linestyle="", label='u MRT linear relaxation')
plt.plot(x/x.max(), u_lin10, color="green", label=r'$u MRT linear relaxation \rho^* = 10$')

# plt.plot(x, u1/u_avg, color="blue", marker="", linestyle="--", label="through the centre of air water interface")
plt.xlabel(r'$x$')
plt.ylabel(r'$u$')

plt.title('Spurious currents')
plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
fig.savefig('spurious_currents.png')
plt.show()
