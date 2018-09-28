

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob, os
import re
import csv
from utilites import remove_duplicates_y, read_data


input_folder_path = os.path.join("../data_for_plots",
                           "interface_shape")

def anal_shape(x_, x0=128, W=20):
    """
    :param x:
    :param x0:
    :param W: interface width
    :return:
    """
    phi_h = 1
    phi_l = 0
    phi_avg = (phi_h+phi_l)/2

    phi_result = phi_avg - 0.5*(phi_h - phi_l)*np.tanh((x_-x0)/(W/2.))
    return x_, phi_result


M = '05'  # 05, 005, 0005

## make plot
plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(12, 8))

x,y =  read_data(os.path.normpath(os.path.join(input_folder_path,"CM_M%s_W20_SOI.csv" % M)), delimiter=',')
plt.plot(x,y,  color="red",  marker=">", linestyle="", label=r'CM SOI')

x,y =  read_data(os.path.normpath(os.path.join(input_folder_path,"CM_M%s_W20_FOI.csv" % M)), delimiter=',')
plt.plot(x,y, color="blue", marker="x", linestyle="", label=r'CM FOI')

x,y =  read_data(os.path.normpath(os.path.join(input_folder_path,"MRT_M%s_W20.csv" % M)), delimiter=',')
plt.plot(x,y, color="brown",  marker="<", linestyle="", label=r'BGK SOI')


x, phi_anal = anal_shape(x)
plt.plot(x, phi_anal,  color="green",  linestyle="-",  marker="", label=r'analytical')


axes = plt.gca()
# axes.set_xlim([0,0.5*1E6])
# axes.set_ylim([0, 1.0])

# plt.plot(frames_cm[0]['arc_length'], frames_cm[0]['PhaseField'], color="green", marker="x", linestyle="",  label='test')
# plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
plt.ylabel(r'$\phi$')
plt.xlabel(r'$x$')

plt.title('interface profile')
plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
plt_file_name = 'interface_profile_W%s_M%s.png' % ( re.sub("\.", '_', str(20)), M)
fig.savefig(plt_file_name)
plt.show()
