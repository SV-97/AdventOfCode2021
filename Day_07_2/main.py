import numpy as np
from numpy.core.fromnumeric import argmin

positions = np.loadtxt("./input.txt", delimiter=",",
                       dtype=np.int64).reshape(-1, 1)
possible_ends = np.arange(
    np.amin(positions), np.amax(positions) + 1).reshape(1, -1)
distances = np.abs(positions - possible_ends)
# Apply the gaussian summation formula to find the total fuel cost expended.
# Note that the integer division by 2 is fine since the numerator
# is always even since it's the product of an even and an odd number (n and n+1).
fuel_cost = ((distances**2 + distances)//2).sum(axis=0)
min_pos = np.argmin(fuel_cost)
min_fuel = fuel_cost[min_pos]

print(min_pos, min_fuel)
