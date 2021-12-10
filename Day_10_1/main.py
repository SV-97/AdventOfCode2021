import re
from collections import deque

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
VALUE_TABLE = {")": 3, "]": 57, "}": 1197, ">": 25137}
score = sum(VALUE_TABLE[match[0]] for line in remainder if (
    match := re.search(CLOSE_RE, line)) is not None)

print(score)
