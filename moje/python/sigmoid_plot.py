import matplotlib.pyplot as plt
import numpy as np

def sigmoid(x):
    """
    :return: velocity profile based on channel height and u_max
    :parameter: u_max - in the middle of the pipe
    It has to match the pressure-inlet pressure-outlet profile
    """

    y = 0.506*np.tanh(5*x-2.5) +0.5

    if y < 0.004: # clip
        y = 0

    if y > 0.996: # clip
        y = 1

    return y


x_max = 1

x = np.linspace(0, x_max, num=100)


y = np.array([ sigmoid(x[i]) for i in range(len(x))])

# make plot
plt.figure(figsize=(12, 8))
plt.plot(x, y, color="red", marker=".", linestyle="-", label='sigmoid')
# plt.plot(x_anal + 25, u_anal/u_avg, color="green", marker=".", linestyle="", label="analytical through  microridge")

plt.xlabel('x')
plt.ylabel('y')


plt.title('Sample Sigmoid')
plt.grid(True)
plt.legend()
plt.show()
