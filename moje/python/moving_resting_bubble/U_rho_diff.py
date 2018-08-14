import matplotlib.pyplot as plt
import os
from utilites import read_data_from_timestep
import numpy as np
import pandas as pd
import csv


folder_path = os.path.join("../data_for_plots", "moving_vs_resting_bubble", "line_data_rho100_v01_circular")

n = 50  # last time-frame

u_diff = np.empty(n)
rho_diff = np.empty(n)

frames_cm = []
frames_mrt = []

for i in range(n):
    frame_cm = pd.read_csv(os.path.join(folder_path, "cm_moving.%d.csv" % i), delimiter="\t")
    frame_mrt = pd.read_csv(os.path.join(folder_path, "mrt_moving.%d.csv" % i), delimiter="\t")

    frames_cm.append(frame_cm)
    frames_mrt.append(frame_mrt)

    u_diff[i] = np.sqrt(sum((frame_cm['U:0'] - frame_mrt['U:0']) * (frame_cm['U:0'] - frame_mrt['U:0']))/len(frame_cm['U:0']))
    rho_diff[i] = np.sqrt(sum((frame_cm['Rho'] - frame_mrt['Rho']) * (frame_cm['Rho'] - frame_mrt['Rho']))/len(frame_cm['Rho']))

# make plot
plt.rcParams.update({'font.size': 24})
# plt.figure(figsize=(12, 8))

frame = 105
# plt.plot(xt_cm[frame], ut_cm[frame], color="red", marker=">", linestyle="-.", label=r'$ u_{cm} \, frame = %d $' % frame)
# plt.plot(xt_mrt[frame], ut_mrt[frame], color="green", marker=">", linestyle="-", label=r'$ u_{mrt} \, frame = %d $' % frame)

fig, ax1 = plt.subplots(figsize=(12, 8))
ax1.plot(np.arange(len(u_diff))*1E3, u_diff, color="blue", linestyle="-", label=r'$\Delta u$')
plt.grid(True)
ax1.set_xlabel(r'iterations')
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel(r'$\Delta u$', color='blue')
ax1.tick_params('y', colors='blue')
ax1.legend(loc=0)
plt.ticklabel_format(style='sci', axis='y', scilimits=(2, 2))

ax2 = ax1.twinx()
ax2.plot(np.arange(len(rho_diff))*1E3, rho_diff, color="green", linestyle="-.", label=r'$\Delta \rho$')
# plt.legend()
ax2.set_ylabel(r'$\Delta \rho$', color='green')
ax2.tick_params('y', colors='green')
ax2.legend(loc=0)
fig.tight_layout()

plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
plt.ticklabel_format(style='sci', axis='y', scilimits=(2, 2))
plt.title('moving bubble')

# plt.text(0.0, 5E-6, r'$\mu^* = %s$' % str(mu_ratio))
fig = plt.gcf()  # get current figure
fig.savefig('moving_vs_resting_bubble.png')
plt.show()

