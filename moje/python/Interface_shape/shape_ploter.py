

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob, os
import re
import csv
from utilites import remove_duplicates_y, read_data


input_folder_path = os.path.join("../data_for_plots",
                           "interface_shape")

def anal_shape(x, x0=128, W=20):
    """
    :param x:
    :param x0:
    :param W: interface width
    :return:
    """
    phi_h = 1
    phi_l = 0
    phi_avg = (phi_h+phi_l)/2

    phi_result = phi_avg - 0.5*(phi_h - phi_l)*np.tanh((x-x0)/(W/2.))
    return x, phi_result

data_CM_M05_W20_SOI = pd.read_csv(os.path.normpath(os.path.join(
    input_folder_path,"CM_M05_W20_SOI.csv")),delimiter=",")

data_CM_M0005_W20_SOI = pd.read_csv(os.path.normpath(os.path.join(
    input_folder_path,"CM_M0005_W20_SOI.csv")),delimiter=",")

data_CM_M05_W20_FOI = pd.read_csv(os.path.normpath(os.path.join(
    input_folder_path,"CM_M05_W20_FOI.csv")),delimiter=",")

data_CM_M0005_W20_FOI = pd.read_csv(os.path.normpath(os.path.join(
    input_folder_path,"CM_M0005_W20_FOI.csv")),delimiter=",")

data_MRT_M05_W20 = pd.read_csv(os.path.normpath(os.path.join(
    input_folder_path,"MRT_M05_W20.csv")),delimiter=",")

data_MRT_M005_W20 = pd.read_csv(os.path.normpath(os.path.join(
    input_folder_path,"MRT_M005_W20.csv")),delimiter=",")



x, phi_anal = anal_shape(data_CM_M05_W20_SOI['arc_length'])

## make plot
plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(12, 8))
# plt.plot(frame_cm_resting['Iteration'][start:stop], frame_cm_resting['F_pressureX'][start:stop], color="red", marker="", linestyle="-.", label='F_pressureX')
# plt.plot(data_CM_M05_W20_SOI['arc_length'], data_CM_M05_W20_SOI['PhaseField'],  color="blue",  marker=">", linestyle="", label=r'CM_M05_W20_SOI')

x1,y1 =  read_data(os.path.normpath(os.path.join(input_folder_path,"CM_M0005_W20_SOI.csv")), delimiter=',')
plt.plot(x1,y1,  color="red",  marker=">", linestyle="", label=r'CM SOI')

# plt.plot(data_CM_M05_W20_FOI['arc_length'], data_CM_M05_W20_FOI['PhaseField'],  color="pink",  marker=".", linestyle="", label=r'CM_M05_W20_FOI')
# plt.plot(data_CM_M0005_W20_FOI['arc_length'], data_CM_M0005_W20_FOI['PhaseField'],  color="blue",  marker="x", linestyle="", label=r'CM FOI')


x1,y1 =  read_data(os.path.normpath(os.path.join(input_folder_path,"CM_M0005_W20_FOI.csv")), delimiter=',')
plt.plot(x1,y1, color="blue", marker="x", linestyle="", label=r'CM FOI')

# plt.plot(data_MRT_M05_W20['arc_length'], data_MRT_M05_W20['PhaseField'],  color="orange",  marker="<", linestyle="", label=r'MRT_M05_W20')

x1,y1 =  read_data(os.path.normpath(os.path.join(input_folder_path,"MRT_M005_W20.csv")), delimiter=',')
plt.plot(x1,y1, color="brown",  marker="<", linestyle="", label=r'BGK SOI')



plt.plot(x, phi_anal,  color="green",  linestyle="-",  marker="", label=r'analytical')


axes = plt.gca()
# axes.set_xlim([0,0.5*1E6])
# axes.set_ylim([0, 1.0])

# plt.plot(frames_cm[0]['arc_length'], frames_cm[0]['PhaseField'], color="green", marker="x", linestyle="",  label='test')
# plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
plt.ylabel(r'$\phi$')
plt.xlabel(r'$x$')

plt.title(r'interface profile')
plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
plt_file_name = 'interface_profile_W%s.png' % re.sub("\.", '_', str(20))
fig.savefig(plt_file_name)
plt.show()
