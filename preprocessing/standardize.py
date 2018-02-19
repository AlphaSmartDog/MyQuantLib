import numpy as np


def dy_min_max(x):
    x = np.array(x)
    x_min = np.min(x)
    x_max = np.max(x)
    return (x - x_min) / (x_max - x_min)


def dy_zscore(x):
    x = np.array(x)
    mean = x.mean()
    std = x.std()
    return (x - mean)/std


def dy_sigmoid(x):
    x = np.array(x)
    return 1. / (1 + np.exp(-x))


def dy_l2norm(x):
    x = np.array(x)
    std = np.sqrt(np.sum(np.power(x, 2)))
    return np.divide(x, std)


def dy_softmax(x):
    x = np.array(x)
    e_x = np.exp(x - np.max(x))
    return e_x / np.sum(e_x)

