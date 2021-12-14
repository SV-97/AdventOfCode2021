import numpy as np
import matplotlib.pyplot as plt


def show(grid):
   # table = {True: "#", False: "."}
    print("\n".join(["".join([x for x in row])
          for row in np.where(grid, "#", ".")]))


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


def scatter_grid(grid):
    y, x = np.where(~grid)
    plt.scatter(x, y, alpha=0.1, marker=".")
    y, x = np.where(grid)
    plt.scatter(x, y)
    _, rxlim = plt.xlim()
    _, rylim = plt.ylim()
    # plt.xlim(-1, max(rxlim, rylim)*1.1)
    # plt.ylim(-1, max(rxlim, rylim)*1.1)
    plt.gca().invert_yaxis()


for (i, (axis, idx)) in enumerate(folds):
    plt.subplot(3, 1, 1)
    scatter_grid(grid)
    if axis == "y":
        if grid.shape[0] % 2 != 0:
            # if the grid isn't even remove the fold line
            grid = np.delete(grid, idx, 0)
        plt.subplot(6, 1, 3)
        upper_half = grid[:grid.shape[0] // 2, :]
        scatter_grid(upper_half)
        plt.subplot(6, 1, 4)
        lower_half = grid[grid.shape[0] // 2:, :]
        scatter_grid(lower_half)
        grid = upper_half | np.flip(lower_half, 0)
    elif axis == "x":
        if grid.shape[1] % 2 != 0:
            # if the grid isn't even remove the fold line
            grid = np.delete(grid, idx, 1)
        plt.subplot(3, 2, 3)
        left_half = grid[:, :grid.shape[1] // 2]
        scatter_grid(left_half)
        plt.subplot(3, 2, 4)
        right_half = grid[:, grid.shape[1] // 2:]
        scatter_grid(right_half)
        grid = left_half | np.flip(right_half, 1)

    plt.subplot(3, 1, 3)
    scatter_grid(grid)
    plt.savefig(f"./img/fold{i}.png")
    plt.close()
    # plt.show()
show(grid)
print("\n")


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
