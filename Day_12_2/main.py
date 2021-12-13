import numpy as np
from multiprocessing import Pool
from copy import deepcopy

with open("./input.txt", "r") as f:
    connections = [line.strip().split("-") for line in f.readlines()]


class Node():
    def __init__(self, name):
        self.big = name[0].isupper()
        self.name = name
        self.connections = set()
        self.remaining_allowed_visits = 1

    def __hash__(self):
        return hash(id(self))

    def __str__(self):
        return self.name

    __repr__ = __str__

    def paths_to_end(self, level=0):
        #print(" ".join([""]*2*level), "Now visiting: ", self, level)
        if self.name == "end":
            return [[self.name]]
        else:
            old_visits = self.remaining_allowed_visits
            if not self.big:
                self.remaining_allowed_visits -= 1
            subpaths = [child.paths_to_end(level+1)
                        for child in self.connections if not child.remaining_allowed_visits == 0]
            self.remaining_allowed_visits = old_visits
            # print(subpaths)
            return [[self.name, *subpath] for x in subpaths for subpath in x]


# set up the graph
nodes = {"start": Node("start"), "end": Node("end")}
for left, right in connections:
    if left not in nodes:
        nodes[left] = Node(left)
    if right not in nodes:
        nodes[right] = Node(right)
    nodes[left].connections.add(nodes[right])
    nodes[right].connections.add(nodes[left])

# make a reference copy - this should be considered
# immutable.
NODES = deepcopy(nodes)


def with_node_twice(node_name):
    nodes = deepcopy(NODES)  # fails for some reason
    node = nodes[node_name]
    if not node.big and node.name not in {"start", "end"}:
        node.remaining_allowed_visits = 2
        twice_node = set(map(tuple,
                             nodes["start"].paths_to_end()))
        node.remaining_allowed_visits = 1
        return twice_node
    else:
        return set()


base = set(map(tuple, nodes["start"].paths_to_end()))

with Pool(24) as p:
    for path in p.map(with_node_twice, [name for name in nodes.keys()]):
        base.update(path)

print(len(base))
