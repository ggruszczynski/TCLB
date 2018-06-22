import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.use('TkAgg')
import csv
import numpy as np
import os
from utilites import remove_duplicates_y, read_data
from numpy.linalg import norm

from two_phase_poiseuille.TwoPhasePoiseuilleAnal import TwoPhasePoiseuilleAnal

rho_l = 10
rho_g = 1
kin_visc_l = 10
kin_visc_g = 1

dyn_visc_l = rho_l * kin_visc_l
dyn_visc_g = rho_g * kin_visc_g
mu_ratio = dyn_visc_l / dyn_visc_g

#
# x_exp_cm, u_exp_cm = read_data(os.path.join("../data_for_plots", "Poiseuille", "diff_Guo_vs_He_Mach0433", "U_Ma0433_Guo.csv"))
# x_exp_mrt, u_exp_mrt = read_data(os.path.join("../data_for_plots", "Poiseuille", "diff_Guo_vs_He_Mach0433", "U_Ma0433_He.csv"))


x_exp_cm_Guo, u_exp_cm_Guo = read_data(os.path.join("../data_for_plots", "Poiseuille", "sharp_Guo_vs_He_vs_MRT_Mach01", "U_sharp_cm_Guo.csv"))
x_exp_cm_He, u_exp_cm_He = read_data(os.path.join("../data_for_plots", "Poiseuille", "sharp_Guo_vs_He_vs_MRT_Mach01", "U_sharp_cm_He.csv"))
x_exp_mrt, u_exp_mrt = read_data(os.path.join("../data_for_plots", "Poiseuille", "sharp_Guo_vs_He_vs_MRT_Mach01", "U_sharp_mrt.csv"))
#





h = 49
uc = 0.00642 # --> max(u) = 0.1

rho_l = 10
rho_g = 1
kin_visc_l = 10
kin_visc_g = 1

dyn_visc_l = rho_l * kin_visc_l
dyn_visc_g = rho_g * kin_visc_g
mu_ratio = dyn_visc_l / dyn_visc_g

y_ = np.linspace(-h, h, 101)
pa = TwoPhasePoiseuilleAnal(u_c=uc, mu_l=dyn_visc_l, mu_g=dyn_visc_g, rho_g=rho_g, rho_l=rho_l, h=h)

print("Body force Gx = %10.2e" % pa.gx)

u = np.array([pa.get_u_profile(y_[i]) for i in range(len(y_))])


pa2 = TwoPhasePoiseuilleAnal(u_c=uc, mu_l=100, mu_g=1, rho_l=100, rho_g=1, h=h)
u2 = np.array([pa2.get_u_profile(y_[i]) for i in range(len(y_))])

# make plot
plt.rcParams.update({'font.size': 24})
plt.figure(figsize=(12, 8))

plt.plot(y_, u, color="green", linestyle="--", label=r'$analytical \, solution$')
# plt.plot(y_, u2, color="blue", linestyle="-.", label=r'$analytical \, solution2$')
# plt.plot(x_exp_cm_Guo - len(x_exp_cm_Guo)/2 + 0.5, u_exp_cm_Guo, color="red", marker=">", linestyle="-", label=r'$cm \, Guo$')  # channel d = 49, thus add 0.5
# plt.plot(x_exp_cm_He - len(x_exp_cm_He)/2 + 0.5, u_exp_cm_He, color="blue", marker="<", linestyle="-.", label=r'$cm \, He$')
# plt.plot(x_exp_mrt - len(x_exp_mrt)/2 + 0.5, u_exp_mrt, color="purple", marker="<", linestyle="-.", label=r'$mrt$')
# plt.plot(x_exp_cm - len(x_exp_cm)/2 + 0.5, u_exp_cm, color="red", marker=">", linestyle="-", label=r'$cm$')
#
plt.xlabel(r'$y$')
plt.ylabel(r'$u_x$')

plt.title('two phase Poiseuille flow')
plt.grid(True)
plt.legend()


# plt.text(0.0, 5E-6, r'$\mu^* = %s$' % str(mu_ratio))
# plt.text(0.0, 5E-6, r'$\rho^* = %s$' % str(rho_l/rho_g))
fig = plt.gcf()  # get current figure
fig.savefig('two_phase_Poiseuille_benchmark_mu%s.png' % str(mu_ratio))
plt.show()

# norm(u_exp_cm_Guo - u)/norm(u)
# norm(u_exp_cm_He - u)/norm(u)
# norm(u_exp_mrt - u)/norm(u)
