from collections import namedtuple
from functools import reduce
from os import stat
import numpy as np
from itertools import product

from numpy.core.fromnumeric import prod

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


class Number():
    def __init__(self, pair, depth):
        self.pair = pair
        self.depth = depth

    @staticmethod
    def from_str(string):
        return Number(np.array([int(x) for x in string if x.isnumeric()]), np.array(collect_depths(parse_pair(string)[0])) - 1)

    def reduce(self):
        self.pair, self.depth = Number.reduce_pair(self.pair, self.depth)
        return self

    @staticmethod
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
            return Number.reduce_pair(pair, depth)
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
            return Number.reduce_pair(pair,depth)
        return pair, depth

    def __add__(self, other):
        pair = np.hstack([self.pair, other.pair])
        depth = np.hstack([self.depth, other.depth]) + 1
        return Number(pair, depth).reduce()

    @staticmethod
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
            return Number.magnitude(pair, depth)

    def __abs__(self):
        self.reduce()
        return Number.magnitude(self.pair, self.depth)[0]


with open("./input.txt", "r") as f:
    numbers = [Number.from_str(line.strip()) for line in f]

magnitudes = [abs(l + r) for l,r in product(numbers, numbers)]

print(max(magnitudes))