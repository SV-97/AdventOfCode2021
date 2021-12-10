import re
from collections import deque
import numpy as np
from statistics import median

with open("./input.txt", "r") as f:
    raw = f.read()


def fixed_point(func, arg):
    """Call f until it converges to some fixed point"""
    while (arg_prime := func(arg)) != arg:
        arg = arg_prime
    return arg_prime


PAIRS_RE = re.compile(r"(\[\])|(\(\))|(\{\})|(\<\>)")
remainder = fixed_point(lambda t: re.sub(PAIRS_RE, "", t), raw).splitlines()

CLOSE_RE = re.compile(r"\]|\)|\}|\>")
valid = [re.search(CLOSE_RE, line) is None for line in remainder]
valid_remainders = (x[1] for x in zip(valid, remainder) if x[0])

score = 0
VALUE_TABLE = {"(": 1, "[": 2, "{": 3, "<": 4}
completion_values = [
    list([VALUE_TABLE[c] for c in line]) for line in valid_remainders]
# if we reversed each line we'd be left with sequences a_k, k=0,...,n
# where n=len(completion string of line)-1. For each line we now want to calculate
# 5(...(5(5(5(a_0) + a_1) + a_2) + a_3)...) + a_n which simplifies to
# 5^n a_0 + 5^(n-1) a_1 + 5^(n-2) a_2 + ... + 5^(n-j) a_j + ... + 5^0 a_n
# Note that by simply not reversing the lines to begin with we can simply take the
# dot product between our sequence and the powers of five.
scores = (np.dot(5**np.arange(0, len(csl)), csl)
          for csl in completion_values)

print(median(scores))
