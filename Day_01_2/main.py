import numpy as np
from itertools import chain


def windows(lst, window_size=2):
    return zip(*[lst[0+k:x if (x := k-window_size+1) != 0 else -1] for k in range(window_size)])
    # chain(, [tuple(lst[-window_size:])])


a1 = list(map(int, open("./input.txt", "r").readlines()))
a2 = list(sum(win) for win in windows(a1, 3))
a3 = np.array(a2)
print(np.sum(np.diff(a3) > 0))
