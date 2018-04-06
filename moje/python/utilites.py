import numpy as np


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