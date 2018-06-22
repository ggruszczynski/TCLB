import matplotlib.pyplot as plt
import csv
import numpy as np
import os
from utilites import remove_duplicates_y




h = 50
uc = 1E-4

rho_l = 1
rho_g = 1
kin_visc_l = 100
kin_visc_g = 1

dyn_visc_l = rho_l * kin_visc_l
dyn_visc_g = rho_g * kin_visc_g
mu_ratio = str(dyn_visc_l / dyn_visc_g)

y_ = np.linspace(-h, h, 1000)
pa = PoiseuilleAnal(u_c=uc, mu_l=dyn_visc_l, mu_g=dyn_visc_g, h=h)
print("Body force Gx = %10.2e" % pa.gx)

u = np.array([pa.get_u_profile(y_[i]) for i in range(len(y_))])

# read experimental data
def read_data(filename):
    x = np.empty(0)
    u = np.empty(0)

    with open(os.path.join("../data_for_plots", "Poiseuille", filename), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        headers = next(reader, None)  # returns the headers or `None` if the input is empty

        for row in reader:
            x = np.append(x, float(row[0]))
            u = np.append(u, float(row[1]))

    x, u = remove_duplicates_y(x, u)
    return x, u


# x_exp_cm, u_exp_cm = read_data("cm_uPoiseuille_v100rho1.csv")
# x_exp_mrt, u_exp_mrt = read_data("mrt_uPoiseuille_v100rho1.csv")
# make plot
plt.rcParams.update({'font.size': 24})
plt.figure(figsize=(12, 8))

plt.plot(y_, u, color="green", linestyle="--", label=r'$analytical \, solution$')
# plt.plot(x_exp_cm - len(x_exp_cm)/2, u_exp_cm, color="red", marker=">", linestyle="-", label=r'$cm$')
# plt.plot(x_exp_mrt - len(x_exp_mrt)/2, u_exp_mrt, color="blue", marker="<", linestyle="-.", label=r'$mrt$')
# plt.plot(y, 2*u, color="red", linestyle="--", label=r'$\mu^* test= %s$' % mu_ratio)

plt.xlabel(r'$y$')
plt.ylabel(r'$u_x$')

plt.title('two phase Poiseuille flow')
plt.grid(True)
plt.legend()


plt.text(0.0, 5E-6, r'$\mu^* = %s$' % mu_ratio)
fig = plt.gcf()  # get current figure
fig.savefig('two_phase_Poiseuille_benchmark_mu%s.png' % mu_ratio)
plt.show()

