import matplotlib.pyplot as plt
import csv
import numpy as np
import os


path = "data_for_plots"

data_pf = "Udata_S30L30.csv"
data_ZhaoHui = "ZhaoHui_Fig3a.csv"
data_ZhaoHui_Rothstein = "ZhaoHui_RothStein_Fig3a.csv"

# data_pf = "Udata_S60L30.csv"
# data_ZhaoHui = "ZhaoHui_Fig3b.csv"
# data_ZhaoHui_Rothstein = "ZhaoHui_Rothstein_Fig3b.csv"

x_pf = np.empty(0)
u_pf = np.empty(0)
u_pf_ridge = np.empty(0)
with open(os.path.join(path, data_pf), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    headers = next(reader, None)  # returns the headers or `None` if the input is empty

    for row in reader:
        x_pf = np.append(x_pf, float(row[0]))
        u_pf = np.append(u_pf, float(row[2]))
        u_pf_ridge = np.append(u_pf_ridge, float(row[3]))


x_ZhaoHui = np.empty(0)
u_ZhaoHui = np.empty(0)
with open(os.path.join(path, data_ZhaoHui), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    headers = next(reader, None)  # returns the headers or `None` if the input is empty

    for row in reader:
        x_ZhaoHui = np.append(x_ZhaoHui, float(row[0]))
        u_ZhaoHui = np.append(u_ZhaoHui, float(row[1]))


x_Rothstein = np.empty(0)
u_Rothstein = np.empty(0)
with open(os.path.join(path, data_ZhaoHui_Rothstein), 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    headers = next(reader, None)  # returns the headers or `None` if the input is empty

    for row in reader:
        x_Rothstein = np.append(x_Rothstein, float(row[0]))
        u_Rothstein = np.append(u_Rothstein, float(row[1]))


def normalize(x, shift=25):
    x -= shift
    x /= max(x)
    return x


def clip_x(x,y, clip=25):
    assert len(x) == len(y)
    indices = []
    for i in range(len(x)):
        if x[i] < clip:
            indices.append(i)

    x = np.delete(x, indices)
    y = np.delete(y, indices)
    return x, y


def remove_duplicates_y(x, y):
    assert len(x) == len(y)
    indices = []
    temp = []

    def attach(t):
        survival_index = int(len(t) / 2)
        t = np.delete(t, survival_index)
        indices.append(t)

    for i in range(0, len(x)-1):
        if y[i] == y[i+1]:
            temp.append(i)
        else:
            if y[i] == y[i - 1]:
                temp.append(i)

            attach(temp)
            temp = []

        if i == (len(x)-2):
            attach(temp)
            temp = []

    indices = [item for sublist in indices for item in sublist]  # flatten list of lists
    # same as
    # for sublist in indices:
    #     for item in sublist:
    #         flat_list.append(item)

    x = np.delete(x, indices)
    y = np.delete(y, indices)
    return x, y


x_pf, u_pf = clip_x(x_pf, u_pf, clip=25)
x_pf = normalize(x_pf, shift=25)
x_pf, u_pf = remove_duplicates_y(x_pf, u_pf)

# make plot
plt.figure(figsize=(12, 8))
plt.plot(x_ZhaoHui, u_ZhaoHui, color="red", marker=".", linestyle="", label='Reference A) [ZhaoHui]')
plt.plot(x_pf, u_pf / max(u_pf), color="blue", marker=".", linestyle="",  label='current model')
plt.plot(x_Rothstein, u_Rothstein, color="green", marker="x", linestyle="",  label='Reference B) [Rothstein]')
plt.xlabel('x')
plt.ylabel('y')

plt.title('Normalized velocity profile \n Channel flow')
plt.grid(True)
plt.legend()

fig = plt.gcf()  # get current figure
fig.savefig('benchmark1.png')

plt.show()
# plt.close(fig)    # close the figure
