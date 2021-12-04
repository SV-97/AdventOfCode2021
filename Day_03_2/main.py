import numpy as np
from math import prod
from functools import reduce


a1 = np.array(list(map(lambda line: np.array([int(i) for i in line.rstrip()]), open(
    "./input.txt", "r").readlines())))
h, w = a1.shape

twos = 2 ** (np.arange(w, 0, -1) - 1)


def int_from_bin(binary_arr):
    return np.dot(binary_arr, twos)


def find_order_commons(order):
    """Let order(x,y) be an order on ints"""
    commons = a1.copy()
    for i in range(w):
        if commons.shape[0] == 1:
            break
        else:
            more_common = order(commons[:, i].sum(
                axis=0), commons.shape[0] / 2)
            commons = commons[commons[:, i] == int(more_common), :]
    return commons


commons = find_order_commons(lambda x, y: x >= y)
uncommons = find_order_commons(lambda x, y: x < y)
oxygen = int_from_bin(commons)
co2_scrubber = int_from_bin(uncommons)
print(oxygen * co2_scrubber)
