import numpy as np
from scipy import optimize
from scipy.interpolate import interp1d

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob, os
import re
import csv
from utilites import remove_duplicates_y, read_data


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

def read_and_trim_data(path, x_low=50, x_high=200):
    x, y = read_data(path, delimiter=',', intepolate=False)
    ind = np.where((x > x_low) & (x < x_high))
    x = x[ind]
    y = y[ind]

    x = (x - x_low)/(x_high-x_low)
    return x,y


# x,y =  read_data(os.path.normpath(os.path.join(input_folder_path,"CM_M%s_W20_SOI.csv" %  re.sub("\.", '', M))), delimiter=',', intepolate=False)
# # xn= np.array(list(filter(lambda x: x > 50 and x <200, x)))
# ind = np.where((x > 100) & (x < 175))
# xn=x[ind]
# yn=y[ind]
#
# ind2 = np.where((yn < 0.95) & (yn > 0.05))
# yn2=yn[ind2]
# xn2=xn[ind2]  # same as xn[(yn < 0.9) & (yn > 0.1)]
#
# print(max(xn2)-min(xn2))


# ymax = max(yn[yn > 0.95])
# ymin = min(yn[yn > 0.95])

## make plot
def make_plot():
    plt.rcParams.update({'font.size': 22})
    plt.figure(figsize=(12, 8))


    x,y = read_and_trim_data(os.path.normpath(os.path.join(input_folder_path,"CM_M%s_W20_SOI.csv" % re.sub("\.", '', M))), x_low, x_high)
    plt.plot(x,y,  color="green",  marker=">", linestyle="", label=r'CM SOI')

    x,y =  read_and_trim_data(os.path.normpath(os.path.join(input_folder_path,"CM_M%s_W20_FOI.csv" % re.sub("\.", '', M))), x_low, x_high)
    plt.plot(x,y, color="blue", marker="", linestyle="-.", label=r'CM FOI')

    x,y =  read_and_trim_data(os.path.normpath(os.path.join(input_folder_path,"SRT_M%s_W20_SOI.csv" % re.sub("\.", '', M))), x_low, x_high)
    plt.plot(x,y, color="red",  marker="<", linestyle="", label=r'SRT SOI')

    x,y =  read_data(os.path.normpath(os.path.join(input_folder_path,"CM_M%s_W20_SOI.csv" %  re.sub("\.", '', M))), delimiter=',', intepolate=False)
    x, phi_anal = anal_shape(x)
    ind = np.where((x > x_low) & (x < x_high))
    x = x[ind]
    phi_anal = phi_anal[ind]
    x = (x - x_low) / (x_high - x_low)

    plt.plot(x, phi_anal,  color="black",  linestyle="-",  marker="", label=r'analytical')


    axes = plt.gca()
    # axes.set_xlim([0,0.5*1E6])
    # axes.set_ylim([0, 1.0])

    # plt.plot(frames_cm[0]['arc_length'], frames_cm[0]['PhaseField'], color="green", marker="x", linestyle="",  label='test')
    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.ylabel(r'$\phi$')
    plt.xlabel(r'$x$')

    plt.title(f'Interface profile: \n %s, M={M}, W=20' % re.sub("\_", ' ', mom_to_relax))
    plt.grid(True)
    plt.legend()

    fig = plt.gcf()  # get current figure
    plt_file_name = 'interface_profile_W%s_M%s.png' % ( 20, re.sub("\.", '', M))
    fig.savefig(plt_file_name)
    plt.show()


def solve(phi_desired, x_guess=128, x0=128, W=20):
    solutions = np.empty(shape=(1,0))

    for phi_d in phi_desired:
        def calc_residua(x_guess):
            (_, result) = anal_shape(x_guess, x0=x0, W=W)
            residua = np.array(phi_d - result)
            return residua

        solution = optimize.root(calc_residua, x_guess, jac=None, tol=1e-6, method='lm')
        solutions= np.append(solutions, solution.x)

    return np.array(solutions)


def solve_from_data(phi_desired, x_data, y_data, x_guess=128):
    solutions = np.empty(shape=(1,0))

    for phi_d in phi_desired:
        def calc_residua(x_guess):

            f = interp1d(x_data, y_data)

            result = f(x_guess)
            residua = np.array(phi_d - result)
            return residua

        solution = optimize.root(calc_residua, x_guess, jac=None, tol=1e-6, method='lm')
        solutions= np.append(solutions, solution.x)

    return np.array(solutions)


W=5
M = '0.5'  # 0.5, 0.05, 0.005
x_low =0
x_high = 256
sensitivity = 0.1
Collision = "CM"  # CM or SRT


mom_to_relax=f"relaxing_1st_moments_W{W}"  # relaxing_1st_moments, relaxing_2nd_moments
input_folder_path = os.path.join("../data_for_plots",
                           "interface_shape",mom_to_relax)

phi_desired=[sensitivity, 1-sensitivity]
x_anal = solve(phi_desired, x_guess=128, x0=128, W=W)

print(x_anal)
width_anal = x_anal[0]-x_anal[1]
print(f"Analytical interface width:{width_anal:.6f}, sensitivity:{100*sensitivity}[%], W:{W}")

x_sim, y_sim = read_data(
    os.path.normpath(os.path.join(input_folder_path, "%s_M%s_W%s_SOI.csv" % (Collision, re.sub("\.", '', M), W))),
    delimiter=',', intepolate=False)

x_sim = solve_from_data(phi_desired, x_sim, y_sim, x_guess=128)

print(x_sim)
width_sim = x_sim[0]-x_sim[1]
print(f"Simulated interface width:{x_sim[0]-x_sim[1]:.6f}, sensitivity:{100*sensitivity}[%], W:{W}")

print(f"Difference:{100*(width_anal-width_sim)/width_anal} [%]")
