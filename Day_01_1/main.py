import numpy as np

converted_input = np.array(
    list(map(int, open("./input.txt", "r").readlines())))
print(np.sum(np.diff(converted_input) > 0))

"""Alternatively

x = list(map(int, open("./input.txt", "r").readlines()))
print(sum(map(lambda x: int(x[1] > x[0]), zip(x[:-2], x[1:]))))

"""
