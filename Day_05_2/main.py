import numpy as np
import re

with open("./input.txt", "r") as f:
    raw = f.read()
string_lines = re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", raw)
lines = np.array([list(map(int, line)) for line in string_lines])
lines = lines.reshape(lines.shape[0], -2, 2)  # (line)×(point)×(coords)


def normalize(lines):
    """normalize such that the lines are in the form
        (low x, low y) -> (high x, high y)
    """
    lx = np.amin(lines[:, :, 0], axis=1)
    hx = np.amax(lines[:, :, 0], axis=1)
    ly = np.amin(lines[:, :, 1], axis=1)
    hy = np.amax(lines[:, :, 1], axis=1)
    p1 = np.vstack([lx, ly]).T
    p2 = np.vstack([hx, hy]).T
    nlines = np.array([[p1[i], p2[i]] for i in range(len(lx))])
    return nlines


def add_hor_or_vert(grid, lines):
    grid = grid.copy()
    for line in normalize(lines):
        grid[line[0, 0]: line[1, 0] + 1, line[0, 1]: line[1, 1] + 1] += 1
    return grid


def add_diag_lines(grid, dlines):
    grid = grid.copy()
    # the slope is either 1 or -1 depending on if the line slopes down or up
    slope = ((dlines[:, 0, 1] - dlines[:, 1, 1]) /
             (dlines[:, 0, 0] - dlines[:, 1, 0])).astype(np.int8)
    for m, line in zip(slope, normalize(dlines)):
        xs = np.arange(line[0, 0], line[1, 0] + 1)
        ys = np.arange(abs(min(m * line[0, 1], m * line[1, 1])),
                       abs(max(m * line[0, 1], m * line[1, 1])) + m, m)
        grid[xs, ys] += 1
    return grid


# filter for those where x1=x2 or y1=y2
hor_or_vert = np.bitwise_or(
    lines[:, 0, 0] == lines[:, 1, 0], lines[:, 0, 1] == lines[:, 1, 1])

grid = np.zeros((np.amax(lines[:, :, 0]) + 1, np.amax(lines[:, :, 1]) + 1))
grid1 = add_hor_or_vert(grid, lines[hor_or_vert])
grid2 = add_diag_lines(grid1, lines[~hor_or_vert])

print(np.sum(grid2 >= 2))
