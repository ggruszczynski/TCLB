

import matplotlib.pyplot as plt
import csv
import numpy as np
import os
from utilites import remove_duplicates_y



textList = ["One", "Two", "Three", "Four", "Five"]


def gen_data(n):
    ts = np.arange(0, n, 1)  # start stop step
    x = np.linspace(0, 2*np.pi, n)
    amplitude = np.sin(x)

    return ts, amplitude

def plot_data(x, y):
    plt.rcParams.update({'font.size': 14})
    plt.figure(figsize=(14, 8))

    plt.plot(x,y, color="red", linestyle="-", linewidth=1)#, label=r'$ eq25$')
    plt.xlabel(r'timestep')
    plt.ylabel(r'y')

    plt.title('Control Signal')
    plt.grid(True)
    #plt.legend()
    # plt.text(0.0, 5E-6, r'$\rho^* = %s$' % rho_ratio)
    fig = plt.gcf()  # get current figure
    fig.savefig('control_signal.png')
    plt.show()


def write_data(filepath, ts, y):
    # with open(filepath, 'w', newline=os.linesep) as csvfile:
    with open(filepath, 'w', newline='\n') as csvfile:  # TCLB needs UNIX lineendings
        filewriter = csv.writer(csvfile,
                                delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL,
                                lineterminator=os.linesep, dialect='unix')

        filewriter.writerow(['timestep','amplitude'])

        for ts, y in zip(ts,y):
            # print(ts, y)
            filewriter.writerow([ts, y])

        csvfile.close()


ts, y = gen_data(10000)

plot_data(ts, y)
write_data('Signal.csv', ts, y)

