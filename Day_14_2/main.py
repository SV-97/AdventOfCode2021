from functools import reduce, lru_cache
from collections import namedtuple, Counter
from main2 import N

with open("input.txt", "r") as f:
    template = f.readline().strip()
    f.readline()  # empty line
    insertions = dict(line.strip().split(" -> ") for line in f.readlines())

codes = [template[i:i+2] for i in range(len(template)-1)]


def resolve(code, n=N-1):
    """
    This does *not* count the code itself.
    In the example we have:
        CH = CB + BH
        HH = HN + NH
        CB = CH + HB
    etc.
    """
    @lru_cache
    def f(args):
        code, levels_to_go = args
        print(code, levels_to_go)
        if levels_to_go == 0:
            return Counter(insertions.get(code, ""))
        else:
            c1 = f((f"{code[0]}{insertions[code]}",
                    levels_to_go - 1)).copy()
            c1.update(
                f((f"{insertions[code]}{code[1]}", levels_to_go - 1)))
            c1.update(f((code, 0)))
            return c1
    return f((code, n))


resolutions = [resolve(code) for code in codes]
c = Counter(template)
for res in resolutions:
    c.update(res)

print(c)
print("Length of resulting string =", sum(c.values()))
print("Difference between most and least common =",
      c.most_common()[0][1] - c.most_common()[-1][1])
