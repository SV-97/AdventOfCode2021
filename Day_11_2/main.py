import numpy as np
from itertools import count

with open("./input.txt", "r") as f:
    raw = f.readlines()
grid = np.array([[int(x) for x in line.strip()]
                for line in raw], dtype=np.uint8)


def resolve_9s(grid, flash_locations):
    # grid = grid.copy()
    new_flash_locations = grid > 9
    tens = np.argwhere(new_flash_locations)
    grid[new_flash_locations] -= 10
    flash_locations |= new_flash_locations
    row_idx, col_idx = np.indices(grid.shape)
    for point in tens:
        max_distance = np.maximum(
            np.abs(row_idx - point[0]), np.abs(col_idx - point[1]))
        # note that a currently flashing octopus can *not* be flashed by it's neighbors
        grid[(max_distance == 1) & (~flash_locations)] += 1
        grid, flash_locations = resolve_9s(grid, flash_locations)
    return grid, flash_locations


for step in count(1):
    grid, flash_locations = resolve_9s(
        grid + 1, np.zeros(grid.shape, np.bool8))
    # print("\n".join("".join(line) for line in grid.astype(str)), "\n")
    if np.all(flash_locations):
        print(step)
        break
