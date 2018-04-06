import matplotlib.pyplot as plt
import csv
import numpy as np

filename = "test.csv"

x = np.empty(0)
y = np.empty(0)

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    headers = next(reader, None)  # returns the headers or `None` if the input is empty

    for row in reader:
        x = np.append(x, float(row[0]))
        y = np.append(y, float(row[1]))

# make plot
plt.figure(figsize=(12, 8))
plt.plot(x, y, color="red", marker=".", linestyle="", label='interface')
# plt.plot(x_anal + 25, u_anal/u_avg, color="green", marker=".", linestyle="", label="analytical through  microridge")

plt.xlabel('x')
plt.ylabel('y')

plt.title('x vs y')
plt.grid(True)
plt.legend()
plt.show()
