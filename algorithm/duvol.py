"""@author: Young
@license: (C) Copyright 2013-2018
@contact: aidabloc@163.com
@file: average.py
@time: 2018/1/30 9:54
"""
import numpy as np


def duvol(x):
    wa = np.convolve(x, [1. / 60] * 60, mode="full")[59:-59]
    x = x[59:]

    buffer = []
    for i in np.arange(60, len(x)):
        mx = x[i - 60:i]
        mwa = wa[i - 60:i]
        mask = mx > mwa
        up = np.sum(np.power((mx - mwa), 2) * mask) / np.sum(mask)
        down = np.sum(np.power((mx - mwa), 2) * (1 - mask)) / np.sum(1 - mask)
        buffer.append(down / up)
    return np.array([np.nan] * 119 + buffer)


def duvol_xx(x, l=60):
    wa = np.convolve(x, [1. / l] * l, mode="full")[l - 1:-l + 1]
    x = x[l - 1:]

    buffer = []
    for i in np.arange(l, len(x)):
        mx = x[i - l:i]
        mwa = wa[i - l:i]
        mask = mx > mwa
        up = np.sum(np.power((mx - mwa), 2) * mask) / np.sum(mask)
        down = np.sum(np.power((mx - mwa), 2) * (1 - mask)) / np.sum(1 - mask)
        buffer.append(down / up)
    return np.array([np.nan] * (2 * l - 1) + buffer)