import matplotlib.pyplot as plt
import os
#from utilites import read_data_from_timestep
import numpy as np
import pandas as pd
import csv


folder_path = os.path.join("../data_for_plots", "moving_vs_resting_bubble", "line_data_rho1_v01_circular")

frames_cm = []
frames_mrt = []

n = np.arange(127, 999, 128)

# n = np.arange(0, 999, 10)
# n = np.arange(127, 256, 128)
i = np.arange(len(n))

u_diff = np.empty(len(n))
rho_diff = np.empty(len(n))

pf_cm_CMx = np.empty(len(n))  # x coordinate of the center of mass of the bubble
pf_mrt_CMx = np.empty(len(n))  # x coordinate of the center of mass of the bubble

for i_, n_ in zip(i, n):
    frame_cm = pd.read_csv(os.path.join(folder_path, "cm_moving.%d.csv" % n_), delimiter="\t")
    frame_mrt = pd.read_csv(os.path.join(folder_path, "mrt_moving.%d.csv" % n_), delimiter="\t")

    frames_cm.append(frame_cm)
    frames_mrt.append(frame_mrt)

    def find_CMx(pf, arc_x, threshold=0.8):

        counter = 0
        weight = 0

        for pf_, x_cm in zip(pf, arc_x):
            if pf_ > threshold:
                counter += x_cm * pf_
                weight += pf_

        ans = counter / weight
        return ans

    pf_cm_CMx[i_] = find_CMx(frame_cm['PhaseField'], frame_cm['arc_length'])
    pf_mrt_CMx[i_] = find_CMx(frame_mrt['PhaseField'], frame_mrt['arc_length'])


theoretical = np.arange(len(n), dtype='float')
theoretical.fill(0.5)
# make plot
plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(12, 8))
plt.plot(n*1E3, pf_cm_CMx/256, color="red", marker="<", linestyle="", label=r'current model')
plt.plot(n*1E3, pf_mrt_CMx/256, color="blue", marker=">", linestyle="", label=r'MRT')
plt.plot(n*1E3, theoretical, color="black", marker="x", linestyle="", label=r'theoretical')

axes = plt.gca()
axes.set_xlim([0, 1E6])
axes.set_ylim([0, 1.0])

# plt.plot(frames_cm[0]['arc_length'], frames_cm[0]['PhaseField'], color="green", marker="x", linestyle="",  label='test')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
plt.ylabel(r'$x_{CM}$')
plt.xlabel(r'$iterations$')

plt.title('Bubble\'s center of the mass')
plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
fig.savefig('x_CM.png')

plt.show()
# plt.close(fig)    # close the figure



# make plot
# plt.rcParams.update({'font.size': 24})
# # plt.figure(figsize=(12, 8))
#
# frame = 105
# # plt.plot(xt_cm[frame], ut_cm[frame], color="red", marker=">", linestyle="-.", label=r'$ u_{cm} \, frame = %d $' % frame)
# # plt.plot(xt_mrt[frame], ut_mrt[frame], color="green", marker=">", linestyle="-", label=r'$ u_{mrt} \, frame = %d $' % frame)
#
# fig, ax1 = plt.subplots(figsize=(12, 8))
# ax1.plot(np.arange(len(u_diff))*1E3, u_diff, color="blue", linestyle="-", label=r'$\Delta u$')
# plt.grid(True)
# ax1.set_xlabel(r'iterations')
# # Make the y-axis label, ticks and tick labels match the line color.
# ax1.set_ylabel(r'$\Delta u$', color='blue')
# ax1.tick_params('y', colors='blue')
# ax1.legend(loc=0)
# plt.ticklabel_format(style='sci', axis='y', scilimits=(2, 2))
#
# ax2 = ax1.twinx()
# ax2.plot(np.arange(len(rho_diff))*1E3, rho_diff, color="green", linestyle="-.", label=r'$\Delta \rho$')
# # plt.legend()
# ax2.set_ylabel(r'$\Delta \rho$', color='green')
# ax2.tick_params('y', colors='green')
# ax2.legend(loc=0)
# fig.tight_layout()
#
# plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
# plt.ticklabel_format(style='sci', axis='y', scilimits=(2, 2))
# plt.title('moving bubble')
#
# # plt.text(0.0, 5E-6, r'$\mu^* = %s$' % str(mu_ratio))
# fig = plt.gcf()  # get current figure
# fig.savefig('moving_vs_resting_bubble.png')
# plt.show()
#
