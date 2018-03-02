import matplotlib.pyplot as plt
import csv
import numpy as np


filename = "velo_profile.csv"

from Poiseuille_num import u_inlet


x = np.empty(0)
u1 = np.empty(0)
u2 = np.empty(0)


with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    headers = next(reader, None)  # returns the headers or `None` if the input is empty

    for row in reader:
        x  = np.append(x,  float(row[0]))
        u1 = np.append(u1, float(row[1]))
        u2 = np.append(u2, float(row[2]))


H = 85  # channel height
R = H / 2
L = 1024  # channel length

x_anal = np.linspace(0, H, len(x)/10)

# u_max = 0.0001307 * 3/2

u_max = max(u2)
# u_avg = np.mean(u2) # bad, takes 0 at wall
u_avg = u_max *2/3
u_anal = np.array([u_inlet(x_anal[i], u_max, R) for i in range(len(x_anal))])

# make plot
plt.figure(figsize=(12, 8))
plt.plot(x, u2/u_avg, color="red", marker=".", linestyle="", label='through microridge')
plt.plot(x_anal + 25, u_anal/u_avg, color="green", marker=".", linestyle="", label="analytical through  microridge")

plt.plot(x, u1/u_avg, color="blue", marker="", linestyle="--", label="through the centre of air water interface")
plt.xlabel('x')
plt.ylabel('y')


plt.title('Velocity profile \n Channel flow')
plt.grid(True)
plt.legend()
plt.show()

