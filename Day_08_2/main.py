import numpy as np
from galois import GF2 as Z2
import re
from collections import Counter

RE = r"(?P<signal_pattern>(?:\w+ ?)+) \| (?P<output_value>(?:\w+ ?)+)"
# This should be an `OrderedDict`` but we're not planning on using anythhing but
# CPython so we'll use this implementation detail for convenience.
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

# We want to interpret the 7-segment display as a 7-dimensional vector over Z/2Z=Z₂.
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


# we directly discard the 8 since it'll always be 1₇ and can't give us any information.
encoded_patterns = to_mat(signal_patterns, False)
encoded_patterns_z2 = Z2(encoded_patterns)

# Note that the output values are the right sides of a linear system.
right_sides = to_mat(output_values, True)
right_sides_z2 = Z2(right_sides)

# the number of ones in each vector - so the length of each code
lengths = np.sum(encoded_patterns, axis=2)

# `l` allows us to look up all the vectors of a certain length
l = [encoded_patterns_z2[lengths == k] for k in range(8)]
l = [x.reshape(len(matches), -1, 7) if x.shape[0]
     > len(matches) else x for x in l]
# `fivers`` and `sixers` are sums over all the codes of length 5/6.
# Summing like this cancels out some unknowns and allows us to
# get some more basis vectors pretty easily.
fivers = l[5].sum(axis=1)
sixers = l[6].sum(axis=1)
# We now calculate all the basis vectors
# (could probably clean this up quite a bit with some algebra)
# This is basically the inverse of the permutation matrix that turns the "right"
# order into the "jumbled" one. There may be some way to get this cheaper.
# Note that by multiplying here we're essentially doing a logical and over our
# 7 segment display segments and by doing addition we're xor-ing.
e_1 = l[3] - l[2]  # a
e_6 = (fivers + sixers) * l[2]  # f
e_3 = l[2] - e_6  # c
e_2 = (l[4] + l[2]) * sixers  # b
e_4 = l[4] - l[2] - e_2  # d
e_7 = l[5].prod(axis=1) - e_1 - e_4  # g
e_5 = fivers + sixers - e_4 - e_6  # e
transform = np.array([e_1, e_2, e_3, e_4, e_5, e_6, e_7])

# This calculates `Z2(transform[:, k, :]) @ right_sides_z2[k].T` for all k.
# Note that we could use `right_sides_z2` here and apply Z2 to `transform``
# directly - but we can't do this because of current limitations in `galois`.
# But given the operations here all play nice with our homomorphism we can
# use the workaround that we've chosen here.
original_encoding_z2 = Z2(transform.swapaxes(0, 1) @
                          right_sides.swapaxes(1, 2))

c = np.array([tuple(encode(k)) for k in CODES])
cs = np.arange(10)

digits = np.array([[x[0] for line in quadruple.T if (x := cs[np.all(line == c, axis=1)]).size > 0]
                   for quadruple in original_encoding_z2])

values = digits @ (10 ** np.arange(3, -1, -1))

print(values.sum())

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
