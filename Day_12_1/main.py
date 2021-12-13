import numpy as np

with open("./input.txt", "r") as f:
    connections = [line.strip().split("-") for line in f.readlines()]


class Node():
    def __init__(self, name):
        self.big = name[0].isupper()
        self.visited = False
        self.name = name
        self.connections = set()

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    __repr__ = __str__

    def number_of_paths_to_end(self, level=0):
        print(" ".join([""]*2*level), "Now visiting: ", self, level)
        if self.name == "end":
            return 1
        else:
            if not self.big:
                self.visited = True
            count = sum(child.number_of_paths_to_end(level+1)
                        for child in self.connections if not child.visited)
            self.visited = False
            return count


nodes = {"start": Node("start"), "end": Node("end")}
for left, right in connections:
    if left not in nodes:
        nodes[left] = Node(left)
    if right not in nodes:
        nodes[right] = Node(right)
    nodes[left].connections.add(nodes[right])
    nodes[right].connections.add(nodes[left])

# remove leaves
nodes = {name: node for (name, node) in nodes.items() if (len(
    node.connections) > 1 or node.name in {"start", "end"}) and not node.big}

print(nodes["start"].number_of_paths_to_end())

# grid = np.array([[int(x) for x in line.strip()]
#                 for line in raw], dtype=np.uint8)
