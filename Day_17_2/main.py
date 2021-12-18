import re
from itertools import count
from math import floor, ceil, sqrt
from functools import lru_cache
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

RE = r"x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)"

with open("./input.txt", "r") as f:
    xl, xm, yl, ym = map(int, re.findall(RE, f.read().strip())[0])

max_steps = 500

xss = []
vx_0s = np.arange(-0, 300)
for vx_0 in vx_0s:
    if vx_0 < 0:
        vx = [min(vx_0 + j, 0) for j in range(max_steps)]
    elif vx_0 >= 0:
        vx = [max(vx_0 - j, 0) for j in range(max_steps)]
    xs = [0, *np.cumsum(vx)]
    xss.append(xs)

yss = []
vy_0s = np.arange(0, 300)
for vy_0 in vy_0s:
    vy = [vy_0 - j for j in range(max_steps)]
    ys = [0, *np.cumsum(vy)]
    yss.append(ys)

xss = np.array(xss)
yss = np.array(yss)

for i, (xs, ys) in enumerate(zip(xss, yss)):
    plt.plot(xs, ys)
    if i == 50:
        break

in_target_box = (xl <= xss) & (xss <= xm) & (yl <= yss) & (yss <= ym)
some_in_target_box = np.any(in_target_box, axis=1)
print(in_target_box.sum())

x_distance_from_box = np.maximum(np.abs(xss - xl), np.abs(xss - xm))
y_distance_from_box = np.maximum(np.abs(yss - yl), np.abs(yss - ym))
# sns.heatmap(xss)
# sns.heatmap(x_distance_from_box + y_distance_from_box)
# sns.heatmap(np.maximum(np.log(x_distance_from_box), np.log(y_distance_from_box)))
# plt.ylim(plt.ylim()[1], plt.ylim()[0])

plt.show()