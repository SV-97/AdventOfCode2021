import re
from itertools import count
from math import floor, ceil, sqrt
from functools import lru_cache

RE = r"x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)"

with open("./input.txt", "r") as f:
    xl, xm, yl, ym = map(int, re.findall(RE, f.read().strip())[0])

"""
First off we note that
x(v(n)) > 0 => x(v(n+1)) >= 0
x(v(n)) = 0 => x(v(n+1)) = 0
x(v(n)) < 0 => x(v(n+1)) <= 0

So our x velocity always converges to 0 after some time.

Furthermore we have
y(v(n+1)) = y(v(n)) - 1 <=> y(v(n)) = y(v(0)) - n
and
y(p(n+1)) = y(p(n)) + y(v(n)) => y(p(n)) = ½n(2y(v(0)) - n + 1)
For some n we need to statisfy
y_l <= y(p(n)) <= y_m
which means
(2yl/n - 1 + n) / 2 <= y(v(0)) <= (2ym/n - 1 + n) / 2
and similarly we find
x(p(n)) = ½n(2x(v(0)) - n + 1) for n <= x(v(0)) and x(p(x(v(0)))) otherwise.
By evaluating x(p) at n=v(0) and checking the bounds inequalities for x_m
we find that x(v(0)) is bounded by
    -½ (1±sqrt(8 x_m)), -½ (1±sqrt(8 x_m))
and n >= upper bound on x(v(0)).
"""

def sgn(x): 
    if x < 0: return -1 
    if x > 0: return 1 
    else: return 0

@lru_cache
def x(n, x_0): 
    if n == 0: return x_0 
    else: return x(n-1, x_0) - sgn(x(n-1, x_0))


xv_bounds = {-(1 - sqrt(8*xm + 1))/2, -(1 - sqrt(8*xl + 1))/2, -(1 + sqrt(8*xm + 1))/2, -(1 + sqrt(8*xl + 1))/2}
xv_bounds = {xv for xv in xv_bounds if xv >= 0} # you have to filter here differently for other values
xv_0l = int(ceil(min(xv_bounds)))
xv_0m = int(floor(max(xv_bounds)))

p = []

for xv_0 in range(xv_0l, xv_0m + 1):
    for n in range(xv_0m, xv_0m + 10_000):
        yv_0l = ceil((2*yl / n - 1 + n) / 2)
        yv_0m = floor((2*ym / n - 1 + n) / 2)
        for yv_0 in range(yv_0l, yv_0m + 1):
            ys = [1/2 * j * (2*yv_0 - j + 1) for j in range(n+1)]
            p.append((xv_0, yv_0, max(ys), n))

print(max(p, key=lambda t: t[1]))