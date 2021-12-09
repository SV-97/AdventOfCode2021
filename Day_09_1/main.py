import numpy as np

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

lows = ((l < 0) | (l > 10)) \
    & ((r < 0) | (r > 10)) \
    & ((a < 0) | (a > 10)) \
    & ((b < 0) | (b > 10))

print((grid[lows] + 1).sum())
