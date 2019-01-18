import matplotlib.pyplot as plt
import csv
import numpy as np
import os
from utilites import remove_duplicates_y



def read_data(filepath):
    x = np.empty(0)
    u = np.empty(0)

    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader, None)  # returns the headers or `None` if the input is empty

        for row in reader:
            x = np.append(x, float(row[0]))
            u = np.append(u, float(row[1]))

    # u = abs(u)
    x, u = remove_duplicates_y(x, u)
    return x, u

# folder = os.path.join("/home","ggruszczynski/","DATA_FOR_PLOTS", "relaxation_interpolation","old_stuff")
# x23, u_eq23_rho10 = read_data(os.path.join(folder, "mrt_u_spurious_eq_23.csv"))
# x25, u_eq25_rho10 = read_data(os.path.join(folder, "mrt_u_spurious_eq_25.csv"))

folder = os.path.join("/home","ggruszczynski/","DATA_FOR_PLOTS", "relaxation_interpolation")
x0, mrt_u_kinvisc = read_data(os.path.join(folder, "parasitic_mrt_kinvisc", "mrt_umag_spurious_kinvisc.csv"))
x1, cm_u_kinvisc = read_data(os.path.join(folder, "parasitic_cm_kinvisc", "cm_umag_spurious_kinvisc.csv"))
x2, cm_u_dynvisc = read_data(os.path.join(folder, "parasitic_cm_dynvisc", "cm_umag_spurious_dynvisc.csv"))

# make plot
plt.rcParams.update({'font.size': 28})
plt.figure(figsize=(14, 8))
# The basic slice syntax is i:j:k where i is the starting index, j is the stopping index, and k is the step

# plt.plot(rho_ratio, u_MRT_Guo, color="red", marker=".", linestyle="", label='u MRT linear relaxation')
# plt.semilogy(x0 / x0.max(), mrt_u_kinvisc.flatten(), marker="<", linestyle="-", color="red")#, label=r'$ eq23$')
plt.semilogy(x1 / x1.max(), cm_u_kinvisc.flatten(), color="black", marker="o", markevery=25, markersize=12, linestyle="-", linewidth=2)#, label=r'$ eq25$')
plt.semilogy(x2 / x2.max(), cm_u_dynvisc.flatten(), color="black", marker="", markevery=25, markersize=12, linestyle="-", linewidth=2)#, label=r'$ eq25$')

plt.xlabel(r'$x$')
plt.ylabel(r'$u_{mag}$ [lu/ts]')

# plt.title('Spurious Currents')
plt.grid(True)
#plt.legend()


# plt.text(0.0, 5E-6, r'$\rho^* = %s$' % rho_ratio)
fig = plt.gcf()  # get current figure
fig.savefig('bw_spurious_currents.pdf', bbox_inches='tight')
plt.show()
