import numpy as np
import re

RE = r"(?P<signal_pattern>(?:\w+ ?)+) \| (?P<output_value>(?:\w+ ?)+)"

with open("./input.txt", "r") as f:
    matches = re.findall(RE, f.read())

signal_patterns, output_values = zip(*matches)

signal_patterns = np.array([s.split(" ") for s in signal_patterns])
output_values = np.array([s.split(" ") for s in output_values])


@np.vectorize
def possible_digits(code):
    lens = {2: 1, 3: 7, 4: 4, 5: (2, 3, 5), 6: (0, 6, 9), 7: 8}
    lens2 = {k: frozenset([v]) if type(v) == int else frozenset(v)
             for (k, v) in lens.items()}
    return lens2[len(code)]


output_digits = possible_digits(output_values)
sure = np.vectorize(len)(output_digits) == 1
print(sure.sum())
