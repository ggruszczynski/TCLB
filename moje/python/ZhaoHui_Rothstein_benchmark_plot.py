import matplotlib.pyplot as plt
import csv
import numpy as np
import os

from utilites import clip_x, normalize, remove_duplicates_y

data_pf = "UdataHQ_rho*54.6_S30L30.csv"
# data_pf = "Udata_rho*54.6_S30L30.csv"

# data_pf = "Udata_rho*820_S30L30.csv"
# data_pf = "UdataHQ_rho*820_S30L30.csv"

data_ZhaoHui = "ZhaoHui_Fig3a.csv"
data_ZhaoHui_Rothstein = "ZhaoHui_RothStein_Fig3a.csv"

# data_pf = "Udata_S60L30.csv"
# data_ZhaoHui = "ZhaoHui_Fig3b.csv"
# data_ZhaoHui_Rothstein = "ZhaoHui_Rothstein_Fig3b.csv"

x_pf = np.empty(0)
u_pf = np.empty(0)
u_pf_ridge = np.empty(0)
with open(os.path.join("data_for_plots","Rothstein", data_pf), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    headers = next(reader, None)  # returns the headers or `None` if the input is empty

    for row in reader:
        x_pf = np.append(x_pf, float(row[0]))
        u_pf = np.append(u_pf, float(row[2]))
        # u_pf_ridge = np.append(u_pf_ridge, float(row[3]))


x_ZhaoHui = np.empty(0)
u_ZhaoHui = np.empty(0)
with open(os.path.join("data_for_plots","Rothstein", data_ZhaoHui), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    headers = next(reader, None)  # returns the headers or `None` if the input is empty

    for row in reader:
        x_ZhaoHui = np.append(x_ZhaoHui, float(row[0]))
        u_ZhaoHui = np.append(u_ZhaoHui, float(row[1]))


x_Rothstein = np.empty(0)
u_Rothstein = np.empty(0)
with open(os.path.join("data_for_plots","Rothstein", data_ZhaoHui_Rothstein), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    headers = next(reader, None)  # returns the headers or `None` if the input is empty

    for row in reader:
        x_Rothstein = np.append(x_Rothstein, float(row[0]))
        u_Rothstein = np.append(u_Rothstein, float(row[1]))

x_pf, u_pf = clip_x(x_pf, u_pf, clip=125)  # 25 or 125
x_pf = normalize(x_pf, shift=125)
x_pf, u_pf = remove_duplicates_y(x_pf, u_pf)

# make plot
plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(12, 8))
plt.plot(x_ZhaoHui, u_ZhaoHui, color="red", marker=".", linestyle="", label='Li et al. (2015)')  # [ZhaoHui]
plt.plot(x_pf, u_pf / max(u_pf), color="blue", marker=".", linestyle="",  label='current model')
plt.plot(x_Rothstein, u_Rothstein, color="green", marker="x", linestyle="",  label='Ou and Rothstein (2005)')  # [Rothstein]
plt.xlabel(r'$y/D$')
plt.ylabel(r'$u/U_{max}$')

# plt.title('Normalized velocity profile \n Channel flow')
plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
fig.savefig('U_rhoHQ54.6_S30L30.png')

plt.show()
# plt.close(fig)    # close the figure
