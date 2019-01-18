from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np


#time = [3570/4302, 4093/4154, 4154/4154]

# CM Total duration: 524.180000 s = 8.736333 min = 0.145606 h
# MRT Total duration: 575.900000 s = 9.598333 min = 0.159972 h
time = [231/309, 262/309, 309/309]
x = np.arange(len(time))

# def millions(x, pos):
#     'The two args are the value and tick position'
#     return '$%1.1fM' % (x * 1e-6)
#
#
# formatter = FuncFormatter(millions)

# fig, ax = plt.subplots()

plt.figure(figsize=(12, 8))
plt.rcParams.update({'font.size': 28})

plt.ylabel(r'$normalized \, time$')


# ax.yaxis.set_major_formatter(formatter)

plt.bar(x, time, color="black", width=0.6)
plt.xticks(x, ('BGK', 'MRT', 'CM'))

plt.grid(True)
# plt.legend()

fig = plt.gcf()  # get current figure
# fig.savefig('Couette_benchmark_100.png')
fig.savefig('CM_MRT_BGK_timing.pdf',  bbox_inches='tight')
plt.show()
