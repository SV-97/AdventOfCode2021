import numpy as np
from math import prod
from functools import reduce


def f(acc, elem):
    print(acc)
    aim, horizontal, depth = acc
    direction, value = elem
    if direction == "down":
        return (aim + value, horizontal, depth)
    elif direction == "up":
        return (aim - value, horizontal, depth)
    elif direction == "forward":
        return (aim, horizontal + value, depth + aim * value)


a1 = map(lambda line: line.split(" "), open("./input.txt", "r").readlines())
a2 = reduce(f, ((t[0], int(t[1])) for t in a1), (0, 0, 0))
print(a2[1] * a2[2])
