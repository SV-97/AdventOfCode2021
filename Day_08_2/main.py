import numpy as np
from galois import GF2 as Z2
import re
from collections import Counter

RE = r"(?P<signal_pattern>(?:\w+ ?)+) \| (?P<output_value>(?:\w+ ?)+)"
CODES = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9}

with open("./input.txt", "r") as f:
    matches = re.findall(RE, f.read())

signal_patterns, output_values = zip(*matches)

# We want to interpret the 7-segment display as a 7-dimensional vector over Z/2Z.
# To do this we start by mapping a-g to e_1, ..., e_7.
ident = np.eye(7, dtype=Z2)
ident_z2 = Z2(np.eye(7, dtype=Z2))
mapping = dict(zip("abcdefg", ident))

# we now encode each of our strings with characters from a-g as a combination
# of our basis vectors.


def encode(string):
    return sum(mapping[char] for char in string)


def to_mat(strings, allow_8=False):
    return np.array(
        [[encode(string) for string in patterns.split(" ") if len(string) != 7 or allow_8] for patterns in strings])


encoded_patterns = to_mat(signal_patterns, False)
encoded_patterns_z2 = Z2(encoded_patterns)

right_sides = to_mat(output_values, True)
right_sides_z2 = Z2(right_sides)


lenghts = np.sum(encoded_patterns, axis=2)
running_sum = 0
c = Counter()
tens = 10 ** np.arange(3, -1, -1)  # powers of ten from 1 to 1000
for i, mat in enumerate(encoded_patterns_z2):
    l = [mat[lenghts[i] == lenf] for lenf in range(8)]
    fivers = l[5].sum(axis=0)
    sixers = l[6].sum(axis=0)
    e_1 = l[3] - l[2]  # a
    e_6 = (fivers + sixers) * l[2]  # f
    e_3 = l[2] - e_6  # c
    e_2 = (l[4] + l[2]) * sixers  # b
    e_4 = l[4] - l[2] - e_2  # d
    e_7 = l[5].prod(axis=0) - e_1 - e_4  # g
    e_5 = fivers + sixers - e_4 - e_6  # e
    transform = [e_1, e_2, e_3, e_4, e_5, e_6, e_7]
    translate = {np.argwhere(transform[k] != 0)[
        0][1]: a for k, a in enumerate("abcdefg")}

    indices = [np.argwhere(lin_comb != 0) for lin_comb in right_sides_z2[i]]
    codes = ["".join(translate[index[0]] for index in index_seq)
             for index_seq in indices]
    digits = [CODES["".join(sorted(code))] for code in codes]
    running_sum += np.dot(tens, np.array(digits))
    c.update(digits)
print(running_sum)
"""
classes:
length | values
    2  | 1
    3  | 7
    4  | 4
    5  | 2, 3, 5
    6  | 0, 6, 9
    7  | 8
"""
