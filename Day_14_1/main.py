from functools import reduce
from collections import namedtuple, Counter

with open("input.txt", "r") as f:
    template = f.readline().strip()
    f.readline()  # empty line
    insertions = dict(line.strip().split(" -> ") for line in f.readlines())


def apply_insertions(template):
    Acc = namedtuple("Accumulator", ["last_letter", "new_string"])

    def f(acc: Acc, new_letter: str):
        code = f"{acc.last_letter}{new_letter}"
        return Acc(new_letter, f"{acc.new_string}{insertions.get(code, '')}{new_letter}")
    return reduce(f, template, Acc("", "")).new_string


for i in range(10):
    template = apply_insertions(template)
    # print(template)

c = Counter(template).most_common()
print(c[0][1] - c[-1][1])
