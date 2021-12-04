import numpy as np
import re

with open("./input.txt", "r") as f:
    num_line = f.readline()
    rem = f.readlines()
blocks = np.array([[[int(x) for x in re.findall(r"\S+", line.rstrip())]
                    for line in rem[k*6+1:k*6+6]] for k in range(len(rem) // 6)])

mask = np.zeros(blocks.shape, np.bool8)
for num in map(int, num_line.split(",")):
    mask |= blocks == num
    match_in_grid = np.any(np.all(mask, axis=1), axis=1) \
        | np.any(np.all(mask, axis=2), axis=1)
    if np.any(match_in_grid):
        winners = np.argwhere(match_in_grid)
        assert(len(winners) == 1)
        winner = winners.flatten()[0]
        unmarked = blocks[winner][~mask[winner]]
        print(num * unmarked.sum())
        break
