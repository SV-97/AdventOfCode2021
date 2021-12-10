import re
from collections import deque

with open("./input.txt", "r") as f:
    raw = f.read()
    # raw_lines = [line.strip() for line in f.readlines()]


def fixed_point(func, arg):
    """Call f until it converges to some fixed point"""
    while (arg_prime := func(arg)) != arg:
        arg = arg_prime
    return arg_prime


PAIRS_RE = re.compile(r"(\[\])|(\(\))|(\{\})|(\<\>)")
remainder = fixed_point(lambda t: re.sub(PAIRS_RE, "", t), raw).splitlines()

CLOSE_RE = re.compile(r"\]|\)|\}|\>")
valid = [re.search(CLOSE_RE, line) is None for line in remainder]
invalid_lines = (x[1] for x in zip(valid, raw.splitlines()) if not x[0])

score = 0
VALUE_TABLE = {")": 3, "]": 57, "}": 1197, ">": 25137}
CORRECT_PAIRS = {tuple(c) for c in ["()", "[]", "{}", "<>"]}
for line in invalid_lines:
    stack = deque([line[0]])
    for i, c in enumerate(line[1:]):
        if c in VALUE_TABLE.keys():
            left = stack.pop()
            if (left, c) not in CORRECT_PAIRS:
                score += VALUE_TABLE[c]
                break
        else:
            stack.append(c)

print(score)
