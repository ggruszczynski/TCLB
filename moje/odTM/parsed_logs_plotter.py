
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob, os
import re
import csv


input_folder_path = os.path.join("./")

input_filename = os.path.normpath(os.path.join(input_folder_path, "parsed_lines_cm.log"))
data = pd.read_csv(os.path.join(input_filename), delimiter="\t")


def filter_data(is_stopped_by_NaN = False):
    filtered_data = data[(data.stopped_by_NaN == is_stopped_by_NaN)]
    ydata = filtered_data['sigma']
    xdata = filtered_data['Viscosity_h']

    return xdata, ydata


not_crashed_dr,  not_crashed_vr = filter_data(is_stopped_by_NaN=False)
crashed_dr,  crashed_vr = filter_data(is_stopped_by_NaN=True)


## make plot
plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(12, 8))
plt.loglog(not_crashed_dr, not_crashed_vr,  color="green",  marker=".", linestyle="", label=r'not crashed')
plt.loglog(crashed_dr, crashed_vr,  color="red",  marker=".", linestyle="", label=r'crashed with NaN')
# plt.plot(np.arange(n)*1E3, mrt_ux_std, color="blue", marker="", linestyle="--", label=r'MRT')
# plt.plot(line_size, theoretical, color="black", marker="x", linestyle="", label='theoretical')

axes = plt.gca()
# axes.set_xlim([0,0.5*1E6])
# axes.set_ylim([0, 1.0])

# plt.plot(frames_cm[0]['arc_length'], frames_cm[0]['PhaseField'], color="green", marker="x", linestyle="",  label='test')
# plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
plt.ylabel(r'$\sigma$')
plt.xlabel(r'$\mu_{liq}$')

plt.title(r'CM Stability')
plt.grid(True)
plt.legend()

#fig = plt.gcf()  # get current figure
#plt_file_name = 'CM_Stability_ux=%s.png' % re.sub("\.", '_', str(VelocityX))
#fig.savefig(plt_file_name)
plt.show()

# plt.close(fig) # close the figure



# is_crashed = data["stopped_by_NaN"]
# df.query('(a < b) & (b < c)')
# df[(df.a < df.b) & (df.b < df.c)]


# d = {
#     'Name': ['Alisa', 'Bobby', 'jodha', 'jack', 'raghu', 'Cathrine',
#              'Alisa', 'Bobby', 'kumar', 'Alisa', 'Alex', 'Cathrine'],
#     'Age': [26, 24, 23, 22, 23, 24, 26, 24, 22, 23, 24, 24],
#
#     'Score': [85, 63, 55, 74, 31, 77, 85, 63, 42, 62, 89, 77]}
#
# df = pd.DataFrame(d, columns=['Name', 'Age', 'Score'])

# df.loc[df['Score'].idxmax()]
