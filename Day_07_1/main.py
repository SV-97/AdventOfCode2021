import numpy as np
from numpy.core.fromnumeric import argmin

positions = np.loadtxt("./input.txt", delimiter=",",
                       dtype=np.int64).reshape(-1, 1)
possible_ends = np.arange(
    np.amin(positions), np.amax(positions) + 1).reshape(1, -1)
distances = np.abs(positions - possible_ends).sum(axis=0)
min_pos = np.argmin(distances)
min_fuel = distances[min_pos]

print(min_pos, min_fuel)
