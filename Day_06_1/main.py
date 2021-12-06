import numpy as np

DAYS = 80

with open("./input.txt", "r") as f:
    raw = f.read()
fish = np.array([int(x) for x in raw.split(",")])


def naive(fish):
    fish = fish.copy()
    for _t in range(DAYS):
        rle = np.array([np.sum(fish == k) for k in range(9)])
        # print(_t, fish, rle)
        mask = fish == 0
        fish[mask] = 7
        fish = np.hstack([fish, 9 * np.ones(np.sum(mask), np.int64)])
        fish -= 1

    return fish.size


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


print(naive(fish))
print(compact(fish))
