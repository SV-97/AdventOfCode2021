import numpy as np
import heapq
from math import prod

with open("./input.txt", "r") as f:
    grid = np.array([[int(c) for c in line.strip()]
                    for line in f.readlines()], dtype=np.int8)

# subtract the left pixel from each pixel.
l = np.hstack([100*np.ones((grid.shape[0], 1), dtype=np.int8),
              grid[:, 1:] - grid[:, :-1]])

# same thing for the right side
r = np.hstack([grid[:, :-1] - grid[:, 1:], 100 *
              np.ones((grid.shape[0], 1), dtype=np.int8)])

# above...
a = np.vstack([100*np.ones((1, grid.shape[1]), dtype=np.int8),
              grid[1:, :] - grid[:-1, :]])
# and below
b = np.vstack([grid[:-1, :] - grid[1:, :], 100 *
              np.ones((1, grid.shape[1]), dtype=np.int8)])

lows = \
    ((l < 0) | (l > 10)) \
    & ((r < 0) | (r > 10)) \
    & ((a < 0) | (a > 10)) \
    & ((b < 0) | (b > 10))

basins = set()
e_1 = np.array([1, 0])
e_2 = np.array([0, 1])
for start in np.argwhere(lows):
    basin = np.zeros(grid.shape, dtype=np.bool8)
    borders = {(start[0], start[1])}
    while len(borders) > 0:
        old_borders = np.array(list(borders))
        basin[old_borders[:, 0], old_borders[:, 1]] = True
        candidates = np.vstack([
            old_borders + e_1,
            old_borders - e_1,
            old_borders + e_2,
            old_borders - e_2])
        # we first discard all those that aren't even on the grid anymore
        valid_candidates = \
            (candidates[:, 0] >= 0) & (candidates[:, 0] < grid.shape[0]) \
            & (candidates[:, 1] >= 0) & (candidates[:, 1] < grid.shape[1])
        v_can = candidates[valid_candidates, :]
        # and now choose all that aren't already part of the basin
        # and have a small enough value.
        valid_candidates[valid_candidates] &= \
            (~basin[v_can[:, 0], v_can[:, 1]]) \
            & (grid[v_can[:, 0], v_can[:, 1]] < 9)
        borders = set(tuple(coords)
                      for coords in candidates[valid_candidates, :])
    # gotta convert to a tuple so we can hash it
    basins.add(tuple(map(tuple, basin)))

largest_3 = heapq.nlargest(3, map(lambda basin: np.array(basin).sum(), basins))
print(prod(largest_3))
