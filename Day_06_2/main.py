import numpy as np

DAYS = 256

# with open("./input.txt", "r") as f:
#     raw = f.read()
# fish = np.array([int(x) for x in raw.split(",")])

fish = np.loadtxt("./input.txt", delimiter=",", dtype=np.uint64)


def compact(fish):
    rle = np.zeros(9, np.uint64)
    rle[:6] = np.array([np.sum(fish == k) for k in range(6)])

    for _t in range(DAYS):
        # print(_t, rle)
        zeros = rle[0]
        rle[:-1] = rle[1:]
        rle[6] += zeros
        rle[8] = zeros

    return np.sum(rle)


print(compact(fish))
