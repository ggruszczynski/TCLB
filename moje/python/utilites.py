import numpy as np
import csv


def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        value_rounded = [round(value[i], 12) for i in range(len(value))]  # 12 decimal digits is enough
        h = hash(tuple(value_rounded))  # convert to tuple, list are un-hashable since they can change order
        if h not in seen:
            output.append(value)
            seen.add(h)
    return output


def normalize(x, shift=25):
    x -= shift
    x /= max(x)
    return x


def clip_x(x, y, clip=25):
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
        if t:  # not empty
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


# read experimental data
def read_data(filepath, delimiter='\t', intepolate=False):
    x = np.empty(0)
    y = np.empty(0)

    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        headers = next(reader, None)  # returns the headers or `None` if the input is empty

        for row in reader:
            x = np.append(x, float(row[0]))
            y = np.append(y, float(row[1]))

    x, y = remove_duplicates_y(x, y)

    if intepolate==True:
        x_max = max(x)
        n= len(x)
        xvals = np.linspace(0, x_max, 10 * n)
        yinterp = np.interp(xvals, x, y)

        x = xvals
        y = yinterp

    return x, y


def read_data_from_timestep(filepath):
    n_rows = None
    with open(filepath, 'r') as file:
        n_rows = len(file.readlines())

    x = np.empty(n_rows)
    u = np.empty(n_rows)
    rho = np.empty(n_rows)

    # x = np.empty(0)
    # u = np.empty(0)
    # rho = np.empty(0)

    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        headers = next(reader, None)  # returns the headers or `None` if the input is empty
        # "0flag"	"1ADDITIONALS"	"2BODY"	"3BOUNDARY"	"4COLLISION"	"5DESIGNSPACE"
        # "6SETTINGZONE"	"7NONE"	"8Rho"	"9PhaseField"
        # "10U:0"	"11U:1"	"12U:2"	"13NormalizedPressure"	"14Pressure"	"15Normal:0"	"16Normal:1"	"17Normal:2"
        # "18vtkValidPointMask"	"19arc_length"	"20Points:0"	"21Points:1"	"22Points:2"
        i = 0
        for row in reader:
            x[i] = float(row[19])
            u[i] = float(row[10])
            rho[i] = float(row[8])

            # x = np.append(x, float(row[19]))
            # u = np.append(u, float(row[10]))
            # rho = np.append(rho, float(row[8]))

            i = i+1

    #x, u = remove_duplicates_y(x, u)
    return x, u, rho

