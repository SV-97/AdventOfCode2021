import numpy as np
from scipy.sparse import dok_matrix

with open("./input.txt", "r") as f:
    lines = [line.strip() for line in f.readlines()]

T = np.uint16

nodes = np.array([[int(x) for x in line] for line in lines], dtype=T)
n_nodes = sum(map(len, lines))
# we now want to find the adjacency matrix for this graph

adj = dok_matrix((n_nodes, n_nodes), dtype=T)
y, x = np.indices(nodes.shape)
linear_idx = np.arange(n_nodes).reshape(nodes.shape)
for (node_idx, (i, j)) in enumerate(zip(y.flatten(), x.flatten())):
    # print(node_idx, i, j, nodes[i, j])
    if j + 1 < nodes.shape[0]:
        adj[node_idx, node_idx+1] = nodes[i, j+1]
        # adj[node_idx+1, node_idx] = nodes[i, j+1]
    if i+1 < nodes.shape[0]:
        adj[node_idx, linear_idx[i+1, j]] = nodes[i+1, j]
        # adj[linear_idx[i+1, j], node_idx] = nodes[i+1, j]

# with np.printoptions(edgeitems=50, linewidth=250):
print(adj.toarray())


def print_as_graphviz_dot(adj):
    x, y = np.indices(adj.shape)
    with open("graph.dot", "w") as f:
        f.write("digraph G {\n")
        f.writelines(f"{i} -> {j} [label=\"{n}\"];\n" for (i,
                     j), n in adj.items() if n != 0)
        f.write("}\n")


# print_as_graphviz_dot(adj)

def find_shortest_path(graph_adj, start_node=0, target_node=n_nodes-1):
    inf = np.iinfo(T).max
    remaining_nodes = np.ones(n_nodes, np.bool8)
    distances = inf * np.ones(n_nodes, dtype=T)
    distances[start_node] = 0
    predecessor = [None] * n_nodes

    while np.any(remaining_nodes):
        print(f"{remaining_nodes.sum()=}")
        shortest_node = np.argmin(np.where(remaining_nodes, distances, inf))

        remaining_nodes[shortest_node] = False
        if shortest_node == target_node:
            break
        neighbors = adj[shortest_node].items()
        for ((_row, column), weight) in neighbors:
            v = column
            if remaining_nodes[v]:
                # distance update
                alternative = distances[shortest_node] + \
                    weight if weight != inf else inf
                if alternative < distances[v]:
                    distances[v] = alternative
                    predecessor[v] = shortest_node
    # assemble the shortest path
    path = [target_node]
    u = target_node
    while predecessor[u] is not None:
        u = predecessor[u]
        path.append(u)
    return list(reversed(path))


sh = find_shortest_path(adj)
print(sh)
path_mask = np.array([[n in sh for n in row] for row in linear_idx])
print(path_mask)
print(nodes[path_mask][1:].sum())
