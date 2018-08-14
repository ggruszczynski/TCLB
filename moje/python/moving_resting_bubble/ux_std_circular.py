import matplotlib.pyplot as plt
import os
from utilites import read_data_from_timestep
import numpy as np
import pandas as pd
import csv


folder_path = os.path.join("../data_for_plots", "moving_vs_resting_bubble", "line_data_rho100_v01_circular")


n = 500  # last time-frame

cm_ux_std = np.empty(n)
mrt_ux_std = np.empty(n)

frames_cm = []
frames_mrt = []

U0 = 0.01  # mean flow velocity

for i in range(n):
    frame_cm = pd.read_csv(os.path.join(folder_path, "cm_moving.%d.csv" % i), delimiter="\t")
    frame_mrt = pd.read_csv(os.path.join(folder_path, "mrt_moving.%d.csv" % i), delimiter="\t")

    frames_cm.append(frame_cm)
    frames_mrt.append(frame_mrt)

    cm_ux_std[i] = np.sqrt(sum((frame_cm['U:0'] - U0) * (frame_cm['U:0'] - U0)) / len(frame_cm['U:0']))
    mrt_ux_std[i] = np.sqrt(sum((frame_mrt['U:0'] - U0) * (frame_mrt['U:0'] - U0)) / len(frame_mrt['U:0']))



## make plot
plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(12, 8))
plt.plot(np.arange(n), cm_ux_std,  color="red",  marker="<", linestyle="", label=r'current model')
plt.plot(np.arange(n), mrt_ux_std, color="blue", marker=">", linestyle="", label=r'MRT')
# plt.plot(line_size, theoretical, color="black", marker="x", linestyle="", label='theoretical')

# plt.plot(frames_cm[150]['arc_length'], frames_cm[150]['U:0'],  color="red",  marker="<", linestyle="", label=r'current model')
# plt.plot(frames_mrt[150]['arc_length'], frames_mrt[150]['U:0'], color="blue", marker=">", linestyle="", label=r'MRT')

axes = plt.gca()
# axes.set_xlim([xmin,xmax])
# axes.set_ylim([0, 1.0])

# plt.plot(frames_cm[0]['arc_length'], frames_cm[0]['PhaseField'], color="green", marker="x", linestyle="",  label='test')
plt.ylabel(r'$\sigma_{ux}$')
plt.xlabel(r'iterations x 1E3')

plt.title(r'$\sigma_{ux}$ ')
plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
fig.savefig('sigma_ux.png')

plt.show()
plt.close(fig) # close the figure