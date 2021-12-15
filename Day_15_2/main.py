import numpy as np
from scipy.sparse import dok_matrix
import multiprocessing as mp

with open("./input.txt", "r") as f:
    lines = [line.strip() for line in f.readlines()]

T = np.uint8

nodes = np.array([[int(x) for x in line] for line in lines], dtype=T)
n_nodes = sum(map(len, lines))

supergrid = [(nodes + i + j) % 10 for i in range(5) for j in range(5)]


def build_adj(nodes):
    adj = dok_matrix((n_nodes, n_nodes), dtype=T)
    y, x = np.indices(nodes.shape)
    linear_idx = np.arange(n_nodes).reshape(nodes.shape)
    for (node_idx, (i, j)) in enumerate(zip(y.flatten(), x.flatten())):
        if j + 1 < nodes.shape[0]:
            adj[node_idx, node_idx+1] = nodes[i, j+1]
        if i+1 < nodes.shape[0]:
            adj[node_idx, linear_idx[i+1, j]] = nodes[i+1, j]
    return adj


def print_as_graphviz_dot(adj):
    x, y = np.indices(adj.shape)
    with open("graph.dot", "w") as f:
        f.write("digraph G {\n")
        f.writelines(f"{i} -> {j} [label=\"{n}\"];\n" for (i,
                     j), n in adj.items() if n != 0)
        f.write("}\n")


def find_shortest_path(graph_adj, start_node=0, target_node=n_nodes-1):
    inf = np.iinfo(T).max
    remaining_nodes = np.ones(n_nodes, np.bool8)
    distances = inf * np.ones(n_nodes, dtype=T)
    distances[start_node] = 0
    predecessor = [None] * n_nodes

    while np.any(remaining_nodes):
        # print(f"{remaining_nodes.sum()=}")
        shortest_node = np.argmin(np.where(remaining_nodes, distances, inf))

        remaining_nodes[shortest_node] = False
        if shortest_node == target_node:
            break
        neighbors = graph_adj[shortest_node].items()
        for ((_row, column), weight) in neighbors:
            v = column
            if remaining_nodes[v]:
                # distance update
                alternative = distances[shortest_node] + \
                    weight if weight != inf else inf
                if alternative < distances[v]:
                    distances[v] = alternative
                    predecessor[v] = shortest_node
    return predecessor, distances


def assemble_shortest_path(predecessor, target_node):
    path = [target_node]
    u = target_node
    while predecessor[u] is not None:
        u = predecessor[u]
        path.append(u)
    return list(reversed(path))


def do_the_thing(nodes):
    adj = build_adj(nodes)
    return find_shortest_path(adj)


if __name__ == "__main__":
    with mp.Pool(25) as pool:
        sols = pool.map(do_the_thing, supergrid)
    # Basic algorithm to solve this day:
    # solve the subproblems as above, then build a new graph where we connect
    # (0,0) to the right/bottom edges of the first subgrid and edgeweights as
    # calculated for this subgrid. Then connect this up to the right and bottom
    # grids and so on. If a single cell has size m×n this should give us a graph
    # with 4(m+n) + 12(2m+n) + 9 (2m+2n) = 46 m + 34 n nodes; so 8000 which is a
    # bit smaller than the graph of the day 1 problem; although it's more highly
    # connected. So we should get our answer in about 2T-3T where T is the run-time
    # of the original problem (given a sufficient number of threads).
