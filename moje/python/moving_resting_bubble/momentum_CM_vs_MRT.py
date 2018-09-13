import matplotlib.pyplot as plt
import glob, os
#from utilites import read_data_from_timestep
import numpy as np
import pandas as pd
import csv


rho_ratio = '1'
v = '01'
folder_path = os.path.join("../data_for_plots",
                           "moving_vs_resting_bubble",
                           "L_shape_rho%s_v%s" % (rho_ratio, v))


frame_cm_resting = pd.read_csv(os.path.join(folder_path, "cm_resting_bubble_Log_P00_00000025.csv"), delimiter=",")
frame_mrt_resting = pd.read_csv(os.path.join(folder_path, "mrt_resting_bubble_Log_P00_00000025.csv"), delimiter=",")
frame_cm_moving = pd.read_csv(os.path.join(folder_path, "cm_moving_bubble_Log_P00_00000025.csv"), delimiter=",")
frame_mrt_moving = pd.read_csv(os.path.join(folder_path, "mrt_moving_bubble_Log_P00_00000025.csv"), delimiter=",")


start = 500
stop = 1000
# make plot
plt.figure(1)
plt.figure(figsize=(18, 14))
plt.rcParams.update({'font.size': 22})

# frame_n = 1

plt.subplot(211)
plt.title('Resting frame')

### CM ###
# plt.plot(frame_cm_resting['Iteration'][start:stop], frame_cm_resting['MomentumX'][start:stop], color="red", marker="", linestyle="-.", label='CM MomentumX')
# plt.plot(frame_cm_resting['Iteration'], frame_cm_resting['MomentumX_afterCol'], color="blue", marker="", linestyle="--", label='MomentumX_afterCol')

plt.plot(frame_cm_resting['Iteration'][start:stop], frame_cm_resting['F_pressureX'][start:stop], color="red", marker="", linestyle="-.", label='F_pressureX')
plt.plot(frame_cm_resting['Iteration'][start:stop], frame_cm_resting['F_surf_tensionX'][start:stop], color="blue", marker="", linestyle="--", label='F_surf_tensionX')
plt.plot(frame_cm_resting['Iteration'][start:stop], frame_cm_resting['F_muX'][start:stop], color="green", marker="", linestyle="-.", label='F_muX')
plt.plot(frame_cm_resting['Iteration'][start:stop], frame_cm_resting['F_total_hydroX'][start:stop], color="orange", marker="", linestyle="--", label='F_total_hydroX')
# plt.plot(frame_cm_resting['Iteration'][start:stop], frame_cm_resting['F_phiX'][start:stop], color="purple", marker="", linestyle="-.", label='F_phiX')

### MRT ###
# plt.plot(frame_mrt_resting['Iteration'][start:stop], frame_mrt_resting['MomentumX'][start:stop], color="red", marker="", linestyle="-", label='MRT MomentumX')
# plt.plot(frame_mrt_resting['Iteration'], frame_mrt_resting['MomentumX_afterCol'], color="blue", marker="", linestyle="--", label='MomentumX_afterCol')

# plt.plot(frame_mrt_resting['Iteration'][start:stop], frame_mrt_resting['F_pressureX'][start:stop], color="red", marker="", linestyle="-.", label='F_pressureX')
# plt.plot(frame_mrt_resting['Iteration'][start:stop], frame_mrt_resting['F_surf_tensionX'][start:stop], color="blue", marker="", linestyle="--", label='F_surf_tensionX')
# plt.plot(frame_mrt_resting['Iteration'][start:stop], frame_mrt_resting['F_muX'][start:stop], color="green", marker="", linestyle="-.", label='F_muX')
# plt.plot(frame_mrt_resting['Iteration'][start:stop], frame_mrt_resting['F_total_hydroX'][start:stop], color="orange", marker="", linestyle="--", label='F_total_hydroX')
# plt.plot(frame_mrt_resting['Iteration'][start:stop], frame_mrt_resting['F_phiX'][start:stop], color="purple", marker="", linestyle="-.", label='F_phiX')

axes = plt.gca()
# axes.set_xlim([xmin,xmax])
# axes.set_ylim([55, 105])
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
plt.ylabel(r'Magnitude')
# plt.xlabel(r'iterations')
plt.grid(True)
plt.legend()



plt.subplot(212)
plt.title(r'Moving frame')
### CM ###
# plt.plot(frame_cm_moving['Iteration'][start:stop], frame_cm_moving['MomentumX'][start:stop], color="red", marker="", linestyle="-.", label='CM MomentumX')
# plt.plot(frame_cm_moving['Iteration'], frame_cm_moving['MomentumX_afterCol'], color="blue", marker="", linestyle="--", label='MomentumX_afterCol')

plt.plot(frame_cm_moving['Iteration'][start:stop], frame_cm_moving['F_pressureX'][start:stop], color="red", marker="", linestyle="-.", label='F_pressureX')
plt.plot(frame_cm_moving['Iteration'][start:stop], frame_cm_moving['F_surf_tensionX'][start:stop], color="blue", marker="", linestyle="--", label='F_surf_tensionX')
plt.plot(frame_cm_moving['Iteration'][start:stop], frame_cm_moving['F_muX'][start:stop], color="green", marker="", linestyle="-.", label='F_muX')
plt.plot(frame_cm_moving['Iteration'][start:stop], frame_cm_moving['F_total_hydroX'][start:stop], color="orange", marker="", linestyle="--", label='F_total_hydroX')
# plt.plot(frame_cm_moving['Iteration'][start:stop], frame_cm_moving['F_phiX'][start:stop], color="purple", marker="", linestyle="-.", label='F_phiX')

### MRT ###
# plt.plot(frame_mrt_moving['Iteration'][start:stop], frame_mrt_moving['MomentumX'][start:stop], color="red", marker="", linestyle="-", label='MRT MomentumX')
# plt.plot(frame_mrt_moving['Iteration'], frame_mrt_moving['MomentumX_afterCol'], color="blue", marker="", linestyle="--", label='MomentumX_afterCol')

# plt.plot(frame_mrt_moving['Iteration'][start:stop], frame_mrt_moving['F_pressureX'][start:stop], color="red", marker="", linestyle="-.", label='F_pressureX')
# plt.plot(frame_mrt_moving['Iteration'][start:stop], frame_mrt_moving['F_surf_tensionX'][start:stop], color="blue", marker="", linestyle="--", label='F_surf_tensionX')
# plt.plot(frame_mrt_moving['Iteration'][start:stop], frame_mrt_moving['F_muX'][start:stop], color="green", marker="", linestyle="-.", label='F_muX')
# plt.plot(frame_mrt_moving['Iteration'][start:stop], frame_mrt_moving['F_total_hydroX'][start:stop], color="orange", marker="", linestyle="--", label='F_total_hydroX')
# plt.plot(frame_mrt_moving['Iteration'][start:stop], frame_mrt_moving['F_phiX'][start:stop], color="purple", marker="", linestyle="-.", label='F_phiX')

axes = plt.gca()
# axes.set_xlim([xmin,xmax])
# axes.set_ylim([55, 105])
plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
plt.ylabel(r'Magnitude')
plt.xlabel(r'iterations')
plt.grid(True)
plt.legend()

# plt.text(0.0, 0.0, r'cm_bubble diam = %.2f' % diam_x_cm_moving[frame_n])

fig = plt.gcf()  # get current figure
plt.tight_layout()
fig.savefig('cm_momentum_rho%s_v%s.png' % (rho_ratio, v))
# plt.subplots_adjust(top=1.55)
plt.show()
#plt.close(fig)    # close the figure

