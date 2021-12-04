import numpy as np
from math import prod
from functools import reduce


def f(acc, elem):
    print(acc)
    aim, horizontal, depth = acc
    direction, value = elem
    if direction == "down":
        return (aim + value, horizontal, depth)
    elif direction == "up":
        return (aim - value, horizontal, depth)
    elif direction == "forward":
        return (aim, horizontal + value, depth + aim * value)


a1 = np.array(list(map(lambda line: np.array([int(i) for i in line.rstrip()]), open(
    "./input.txt", "r").readlines())))
h, w = a1.shape
ones = a1.sum(axis=0) > h / 2
zeros = np.bitwise_not(ones)
twos = 2 ** (np.arange(w, 0, -1) - 1)
gamma = np.dot(ones, twos)
epsilon = np.dot(zeros, twos)
print(gamma * epsilon)
