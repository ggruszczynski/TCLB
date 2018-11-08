
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob, os
import re
import csv


input_folder_path = os.path.join("../data_for_plots",
                           "slurm_logs", )

input_filename = os.path.normpath(os.path.join(input_folder_path,"parsed_logs", "parsed_lines_mrt.log"))
data = pd.read_csv(os.path.join(input_filename), delimiter="\t")


# def filter_data(velocity_x=0.01, is_stopped_by_NaN = False):
#     filtered_data = data[(data.VelocityX == velocity_x) & (data.stopped_by_NaN == is_stopped_by_NaN)]
#     density_ratio = filtered_data['Density_h'] / filtered_data['Density_l']
#     viscosity_ratio = filtered_data['Viscosity_h'] / filtered_data['Viscosity_l']
#
#     return density_ratio, viscosity_ratio

def filter_data(is_stopped_by_NaN = False, Density_h=1.0, Density_l=1.0):
    filtered_data = data[(data.Density_h == Density_h) & (data.Density_l == Density_l) & (data.stopped_by_NaN == is_stopped_by_NaN)]
    x = filtered_data['VelocityX']
    y = filtered_data['Viscosity_h']

    return x, y


not_crashed_x, not_crashed_y = filter_data(is_stopped_by_NaN=False)
crashed_x, crashed_y = filter_data(is_stopped_by_NaN=True)


## make plot
plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(12, 8))
plt.loglog(not_crashed_x, not_crashed_y, color="green", marker=".", linestyle="", label=r'not crashed')
plt.loglog(crashed_x, crashed_y, color="red", marker=".", linestyle="", label=r'crashed with NaN')
# plt.plot(np.arange(n)*1E3, mrt_ux_std, color="blue", marker="", linestyle="--", label=r'MRT')
# plt.plot(line_size, theoretical, color="black", marker="x", linestyle="", label='theoretical')

axes = plt.gca()
# axes.set_xlim([0,0.5*1E6])
# axes.set_ylim([0, 1.0])

# plt.plot(frames_cm[0]['arc_length'], frames_cm[0]['PhaseField'], color="green", marker="x", linestyle="",  label='test')
# plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

plt.ylabel(r'$Viscosity_h$')
plt.xlabel(r'$VelocityX$')


plt.title(r'MRT Stability')
plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
plt_file_name = 'MRT_Stability.png' # % re.sub("\.", '_', str(VelocityX))
fig.savefig(plt_file_name)
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