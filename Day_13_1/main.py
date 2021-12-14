import numpy as np


def show(grid):
    table = {True: "#", False: "."}
    print("\n".join(["".join([table[entry] for entry in row])
          for row in grid]))


coords = np.loadtxt("./input.txt", delimiter=",", dtype=np.int32)
coords[:, [0, 1]] = coords[:, [1, 0]]
with open("input2.txt", "r") as f:
    folds = [((x := line.strip().split("="))[0][-1], int(x[-1]))
             for line in f.readlines()]

original_width = np.amax(coords[:, 1]) + 1
original_height = np.amax(coords[:, 0]) + 1
original_size = np.array([original_height, original_width])

grid = np.zeros(original_size, np.bool8)
for coord in coords:
    grid[coord[0], coord[1]] = True

for (axis, idx) in folds:
    if axis == "y":
        if grid.shape[0] % 2 != 0:
            # if the grid isn't even remove the fold line
            grid = np.delete(grid, idx, 0)
        upper_half = grid[:grid.shape[0] // 2, :]
        lower_half = grid[grid.shape[0] // 2:, :]
        print(upper_half, "\n", lower_half)
        grid = upper_half | np.flip(lower_half, 0)
    elif axis == "x":
        if grid.shape[1] % 2 != 0:
            # if the grid isn't even remove the fold line
            grid = np.delete(grid, idx, 1)
        left_half = grid[:, :grid.shape[1] // 2]
        right_half = grid[:, grid.shape[1] // 2:]
        grid = left_half | np.flip(right_half, 1)
    break

print(np.sum(grid))
# show(grid)

"""

for fold in folds:
    axis, idx = fold
    b_1 = original_size[axis] - coords[coords[:, axis] >= idx][:, axis]
    b_2 = coords[coords[:, 0] >= axis][:, 1-axis]
    if axis == 0:
        folded = [b_1, b_2]
    else:
        folded = [b_2, b_1]
    new_coords = np.vstack([coords[coords[:, axis] < idx], np.hstack(folded)])
"""
