import numpy as np
from math import prod

directions = {"forward": np.array([1, 0]), "down": np.array(
    [0, 1]), "backward": np.array([-1, 0]), "up": np.array([0, -1])}

a1 = map(lambda line: line.split(" "), open("./input.txt", "r").readlines())
a2 = sum([int(t[1]) * directions[t[0]] for t in a1])
print(prod(a2))
