from collections import namedtuple
from functools import reduce
import numpy as np


Pair = namedtuple("Pair", ["left", "right", "depth"])


def parse_pair(string, depth=0):
    if string[1].isnumeric():
        left = int(string[1])
        length_left = 1
    elif string[1] == "[":
        left, length_left = parse_pair(string[1:], depth + 1)

    if string[2+length_left].isnumeric():
        right = int(string[2+length_left])
        length_right = 1
    elif string[2+length_left] == "[":
        right, length_right = parse_pair(string[2+length_left:], depth + 1)
    return Pair(left, right, depth), 3 + length_left + length_right


def collect_depths(pair):
    if type(pair.left) == int:
        l = [pair.depth + 1]
    else:
        l = collect_depths(pair.left)
    if type(pair.right) == int:
        r = [pair.depth + 1]
    else:
        r = collect_depths(pair.right)
    return [*l, *r]


def reduce_pair(pair, depth):
    # print(f"{pair=}, {depth=}")
    idx = np.where(depth >= 4)[0]
    if len(idx) > 0: # explode
        i = idx[0]
        # print("explode")
        if i >= 1:
            pair[i-1] += pair[i]
        if i+2 < len(pair):
            pair[i+2] += pair[i+1]
        pair[i] = 0
        depth[[i, i+1]] -= 1
        pair = np.delete(pair, i+1)
        depth = np.delete(depth, i+1)
        return reduce_pair(pair, depth)
    idx = np.where(pair >= 10)[0]
    if len(idx) > 0: # split
        # print("split")
        i = idx[0]
        l = int(np.floor(pair[i] / 2))
        r = int(np.ceil(pair[i] / 2))
        pair[i] = l
        pair = np.insert(pair, i+1, r)
        depth = np.insert(depth, i+1, depth[i] + 1)
        depth[i] += 1
        return reduce_pair(pair,depth)
    return pair, depth


def add(left_pair, left_depth, right_pair, right_depth):
    pair = np.hstack([left_pair, right_pair])
    depth = np.hstack([left_depth, right_depth]) + 1
    return pair, depth


with open("./input.txt", "r") as f:
    pairs = []
    depths = []
    for line in f:
        pairs.append(np.array([int(x) for x in line.strip() if x.isnumeric()]))
        depths.append(np.array(collect_depths(parse_pair(line.strip())[0])) - 1) # -1 because we wanna start at 0


p = pairs[0]
d = depths[0]
for pair, depth in zip(pairs[1:], depths[1:]):
    p, d = reduce_pair(*add(p, d, pair, depth))

print(p)
print(d)

def magnitude(pair, depth):
    if len(pair) == 1:
        return pair
    else:
        i = np.argmax(depth)
        l = 3 * pair[i]
        r = 2 * pair[i+1]
        pair[i] = l + r
        depth[i] -= 1
        pair = np.delete(pair, i+1)
        depth = np.delete(depth, i+1)
        return magnitude(pair, depth)

print(magnitude(p, d))