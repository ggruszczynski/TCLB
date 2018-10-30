import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker

from matplotlib.ticker import EngFormatter
from matplotlib.ticker import ScalarFormatter

import glob, os
#from utilites import read_data_from_timestep
import numpy as np
import pandas as pd
import csv


rho_ratio = '10'
v = '001'
# folder_path = os.path.join("../data_for_plots",
#                            "moving_vs_resting_bubble",
#                            "forces_L_shape_rho%s_v%s" % (rho_ratio, v))

folder_path = os.path.join("../data_for_plots",
                           "moving_vs_resting_bubble",
                           "forces_L_shape_rho%s_v%s_U01" % (rho_ratio, v))

# rho_ratio = '1'
# v = '001'
# folder_path = os.path.join("../data_for_plots",
#                            "moving_vs_resting_bubble",
#                            "forces_rho%s_v%s_circular_U01_GF" % (rho_ratio, v))

# folder_path = os.path.join("../data_for_plots",
#                            "moving_vs_resting_bubble",
#                            "forces_rho%s_v%s_oscillating_U01_GF" % (rho_ratio, v))
#

frame_cm_resting = pd.read_csv(os.path.join(folder_path, "cm_resting_bubble_Log_P00_00000025.csv"), delimiter=",")
frame_mrt_resting = pd.read_csv(os.path.join(folder_path, "mrt_resting_bubble_Log_P00_00000025.csv"), delimiter=",")
frame_cm_moving = pd.read_csv(os.path.join(folder_path, "cm_moving_bubble_Log_P00_00000025.csv"), delimiter=",")
frame_mrt_moving = pd.read_csv(os.path.join(folder_path, "mrt_moving_bubble_Log_P00_00000025.csv"), delimiter=",")


def make_plot(frame_moving, frame_resting, plot_name):
    start = 500
    stop = 1000
    # make plot
    plt.figure(1)
    plt.figure(figsize=(18, 14))
    plt.rcParams.update({'font.size': 26})

    # frame_n = 1

    plt.subplot(211)
    plt.title('Resting frame %s' % plot_name)

    ### CM ###

    # plt.plot(frame_cm_resting['Iteration'][start:stop], frame_cm_resting['MomentumX'][start:stop], color="red", marker="", linestyle="-.", label='CM MomentumX')
    # plt.plot(frame_cm_resting['Iteration'], frame_cm_resting['MomentumX_afterCol'], color="blue", marker="", linestyle="--", label='MomentumX_afterCol')

    plt.plot(frame_resting['Iteration'][start:stop], frame_resting['F_pressureX'][start:stop], color="red", marker="", linestyle="-.", label=r'$F_{X, p}$')  # pressure
    plt.plot(frame_resting['Iteration'][start:stop], frame_resting['F_surf_tensionX'][start:stop], color="blue", marker="", linestyle="--", label=r'$F_{X, s}$')  #
    plt.plot(frame_resting['Iteration'][start:stop], frame_resting['F_muX'][start:stop], color="green", marker="", linestyle=":", label=r'$F_{X, \mu}$')
    plt.plot(frame_resting['Iteration'][start:stop], frame_resting['F_total_hydroX'][start:stop], color="brown", marker="", linestyle="-", label=r'$F_{X, total}$')

    # plt.plot(frame_resting['Iteration'][start:stop], frame_resting['F_phiX'][start:stop], color="purple", marker="", linestyle="-", label=r'$F_{X, \phi}$')

    axes = plt.gca()
    # axes.set_xlim([xmin,xmax])
    # axes.set_ylim([55, 105])
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(1, 1))
    plt.ylabel(r'Magnitude')
    # plt.xlabel(r'iterations')
    plt.grid(True)
    plt.legend(loc='upper right')


    plt.subplot(212)
    plt.title('Moving frame %s' % plot_name)

    ### SECND PLOT ###
    # plt.plot(frame_cm_moving['Iteration'][start:stop], frame_cm_moving['MomentumX'][start:stop], color="red", marker="", linestyle="-.", label='CM MomentumX')
    # plt.plot(frame_cm_moving['Iteration'], frame_cm_moving['MomentumX_afterCol'], color="blue", marker="", linestyle="--", label='MomentumX_afterCol')

    plt.plot(frame_moving['Iteration'][start:stop], frame_moving['F_pressureX'][start:stop], color="red", marker="", linestyle="-.", label=r'$F_{X, p}$')
    plt.plot(frame_moving['Iteration'][start:stop], frame_moving['F_surf_tensionX'][start:stop], color="blue", marker="", linestyle="--", label=r'$F_{X, s}$')
    plt.plot(frame_moving['Iteration'][start:stop], frame_moving['F_muX'][start:stop], color="green", marker="", linestyle=":", label=r'$F_{X, \mu}$')
    plt.plot(frame_moving['Iteration'][start:stop], frame_moving['F_total_hydroX'][start:stop], color="brown", marker="", linestyle="-", label=r'$F_{X, total}$')

    # plt.plot(frame_moving['Iteration'][start:stop], frame_moving['F_phiX'][start:stop], color="purple", marker="", linestyle="-", label=r'$F_{X, \phi}$')


    # axes = plt.gca()
    # axes.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(0.1E-4))
    # axes.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    # axes.set_xlim([xmin,xmax])
    # axes.set_ylim([55, 105])

    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(1, 1))
    plt.ylabel(r'Magnitude')
    plt.xlabel(r'iterations')
    plt.grid(True)
    plt.legend(loc='upper right')

    # plt.text(0.0, 0.0, r'cm_bubble diam = %.2f' % diam_x_cm_moving[frame_n])

    fig = plt.gcf()  # get current figure
    plt.tight_layout()
    fig.savefig('%s_forces_rho%s_v%s.png' % (plot_name, rho_ratio, v))
    # plt.subplots_adjust(top=1.55)
    plt.show()
    plt.close(fig)    # close the figure

#
make_plot(frame_cm_moving, frame_cm_resting, plot_name="cm_hydro_GF")
make_plot(frame_mrt_moving, frame_mrt_resting, plot_name="mrt_hydro_GF")

# make_plot(frame_cm_moving, frame_cm_resting, plot_name="cm_pf_GF_circular_bubble")
# make_plot(frame_mrt_moving, frame_mrt_resting, plot_name="mrt_pf_GF_circular_bubble")
