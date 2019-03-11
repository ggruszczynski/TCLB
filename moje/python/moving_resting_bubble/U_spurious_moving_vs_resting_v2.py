import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import csv
import re

rho_ratio = '1'
v = '01'
U = '0.01'
Uf = float(U)
Ustr = re.sub("\.", '', U)
folder_path = os.path.join("/media/grzegorz/Container/DATA_FOR_PLOTS",
                           "moving_vs_resting_bubble",
                           f"rho{rho_ratio}_v{v}_circular_U{Ustr}",
                           "line_data")

# folder_path = os.path.join("line_data")
domain_size = 256
frame_n = 999  # last time-frame

frame_cm_resting = pd.read_csv(os.path.join(folder_path, "cm_resting.%d.csv" % frame_n), delimiter=",")
frame_mrt_resting = pd.read_csv(os.path.join(folder_path, "mrt_resting.%d.csv" % frame_n), delimiter=",")
frame_cm_moving = pd.read_csv(os.path.join(folder_path, "cm_moving.%d.csv" % frame_n), delimiter=",")
frame_mrt_moving = pd.read_csv(os.path.join(folder_path, "mrt_moving.%d.csv" % frame_n), delimiter=",")

u_cm = np.sqrt(frame_cm_resting['U:0'] * frame_cm_resting['U:0'] + frame_cm_resting['U:1'] * frame_cm_resting['U:1'])
u_mrt = np.sqrt(
    frame_mrt_resting['U:0'] * frame_mrt_resting['U:0'] + frame_mrt_resting['U:1'] * frame_mrt_resting['U:1'])


# make plot
def make_plot(x1, y1, x2, y2, fig_name, y_label):
    from matplotlib.ticker import FormatStrFormatter

    plt.rcParams.update({'font.size': 32})
    plt.figure(figsize=(14, 8))


    def smooth(x):
        # return x
        #         x = abs(x)
        return x[0:len(x):4]

    axes = plt.gca()
    plt.plot(smooth(x1), smooth(y1), color="black", marker="", markevery=10, markersize=15, linestyle="-", linewidth=2, label='current model')
    # yll = -2.*1E-7
    # yhl = 2.*1E-7

    # plt.plot(smooth(x2), smooth(y2), color="black", marker="", linestyle="-", linewidth=2, label='MRT')
    # yll = -1.5 * 1E-5
    # yhl = -1 * 1E-5
    # axes.set_yticks(np.linspace(yll, yhl, 5))
    # axes.set_ylim([yll, yhl])

    # plt.yscale('log')
    plt.xlim(x1.min(), x1.max())
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.xlabel(r'x/L')
    plt.ylabel(y_label)
    plt.legend()
    plt.grid()

    fig = plt.gcf()  # get current figure
    fig.savefig(fig_name, bbox_inches='tight')
    plt.show()
    plt.close(fig)  # close the figure


make_plot(x1=frame_cm_resting['arc_length']/domain_size, y1=frame_cm_resting['U:0'],
          x2=frame_mrt_resting['arc_length']/domain_size, y2=frame_mrt_resting['U:0'],
          fig_name=f'spurious_currents_CM_vs_MRT_rho{rho_ratio}_v{v}_U{Ustr}_resting_frame.pdf',
          y_label=r'$u_{x}$ [lu/ts]'
         )

# make_plot(x1=frame_cm_moving['arc_length'] / domain_size, y1=frame_cm_moving['U:0'] - Uf,
#           x2=frame_mrt_moving['arc_length'] / domain_size, y2=frame_mrt_moving['U:0'] - Uf,
#           fig_name=f'spurious_currents_CM_vs_MRT_rho{rho_ratio}_v{v}_U{Ustr}_moving_frame.pdf',
#           y_label=r'$(u_{x} - \overline{u_x})$ [lu/ts]'
#           )
