import numpy as np
import re

with open("./input.txt", "r") as f:
    raw = f.read()
string_lines = re.findall(r"(\d+),(\d+) -> (\d+),(\d+)", raw)
lines = np.array([list(map(int, line)) for line in string_lines])
lines = lines.reshape(lines.shape[0], -2, 2)  # (line)×(point)×(coords)

# filter for those where x1=x2 or y1=y2
lines = lines[np.bitwise_or(
    lines[:, 0, 0] == lines[:, 1, 0], lines[:, 0, 1] == lines[:, 1, 1])]
# normalize such that the lines are in the form (low x, low y) -> (high x, high y)
lx = np.amin(lines[:, :, 0], axis=1)
hx = np.amax(lines[:, :, 0], axis=1)
ly = np.amin(lines[:, :, 1], axis=1)
hy = np.amax(lines[:, :, 1], axis=1)
p1 = np.vstack([lx, ly]).T
p2 = np.vstack([hx, hy]).T
nlines = np.array([[p1[i], p2[i]] for i in range(len(lx))])

grid = np.zeros((np.amax(lines[:, :, 0]) + 1, np.amax(lines[:, :, 1]) + 1))
for line in nlines:
    grid[line[0, 0]: line[1, 0] + 1, line[0, 1]: line[1, 1] + 1] += 1

print(np.sum(grid >= 2))
