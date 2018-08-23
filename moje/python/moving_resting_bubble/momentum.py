import matplotlib.pyplot as plt
import glob, os
#from utilites import read_data_from_timestep
import numpy as np
import pandas as pd
import csv


rho_ratio = '1'
v = '01'
folder_path= os.path.join("../data_for_plots",
                           "moving_vs_resting_bubble",
                           "L_shape_rho%s_v%s" % (rho_ratio, v))

frame_cm_resting = pd.read_csv(os.path.join(folder_path, "cm_resting_bubble_Log_P00_00000025.csv"), delimiter=",")
frame_mrt_resting = pd.read_csv(os.path.join(folder_path, "mrt_resting_bubble_Log_P00_00000025.csv"), delimiter=",")
frame_cm_moving = pd.read_csv(os.path.join(folder_path, "cm_moving_bubble_Log_P00_00000025.csv"), delimiter=",")
frame_mrt_moving = pd.read_csv(os.path.join(folder_path, "mrt_moving_bubble_Log_P00_00000025.csv"), delimiter=",")

plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(12, 8))
plt.plot(frame_cm_resting['Iteration'], frame_cm_resting['MomentumX'],  color="red",  marker="", linestyle="-.", label=r'current model')
plt.plot(frame_mrt_resting['Iteration'], frame_mrt_resting['MomentumX'], color="blue", marker="", linestyle="--", label=r'MRT')
# plt.plot(frame_cm_resting['Iteration'], frame_cm_resting['MomentumY'],  color="red",  marker="", linestyle="-.", label=r'current model')
# plt.plot(frame_mrt_resting['Iteration'], frame_mrt_resting['MomentumY'], color="blue", marker="", linestyle="--", label=r'MRT')


# plt.plot(frame_cm_moving['Iteration'], frame_cm_moving['MomentumX'],  color="red",  marker="", linestyle="-.", label=r'current model')
# plt.plot(frame_mrt_moving['Iteration'], frame_mrt_moving['MomentumX'], color="blue", marker="", linestyle="--", label=r'MRT')
# # plt.plot(frame_cm_moving['Iteration'], frame_cm_moving['MomentumY'],  color="red",  marker=">", linestyle="-.", label=r'current model')
# # plt.plot(frame_mrt_moving['Iteration'], frame_mrt_moving['MomentumY'], color="blue", marker="<", linestyle="--", label=r'MRT')
# #

# plt.plot(line_size, theoretical, color="black", marker="x", linestyle="", label='theoretical')

# plt.plot(frames_cm[150]['arc_length'], frames_cm[150]['U:0'],  color="red",  marker="<", linestyle="", label=r'current model')
# plt.plot(frames_mrt[150]['arc_length'], frames_mrt[150]['U:0'], color="blue", marker=">", linestyle="", label=r'MRT')

axes = plt.gca()
# axes.set_xlim([0,0.5*1E6])
# axes.set_ylim([0, 1.0])

plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
plt.ylabel(r'MomentumX')
plt.xlabel(r'iterations')

plt.title(r'MomentumX ')
plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
fig.savefig('momentum_rho%s_v%s.png' % (rho_ratio, v))
plt.show()
plt.close(fig) # close the figure