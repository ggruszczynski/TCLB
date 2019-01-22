from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np


time = np.array([3221, 3749, 3307])  # [s]
time = time / max(time)
x = np.arange(len(time))

plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 32})

plt.ylabel('normalized time')
plt.bar(x, time, color="black", width=0.7)
plt.xticks(x, ('SRT', 'MRT', 'CM'))

plt.grid(True)
# plt.legend()

fig = plt.gcf()  # get current figure
fig.savefig('CM_MRT_SRT_timing.pdf', bbox_inches='tight')
plt.show()
