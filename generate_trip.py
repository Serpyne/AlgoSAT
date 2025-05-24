"""
Inputs:
- ~~Destination (T)~~ (OMITTED)
- Edge weights (Distance between destination)
- Orders [Location, Net Weight]
"""

# -- Constants --
SOURCE = "Perth"
F = 150

from taxicab_distances import generate_nodes, generate_edges

nodes = generate_nodes()
edges = generate_edges()

def neighbours(node):
    n = []
    for edge in edges:
        if edge[0] == node:
            n.append(edge[1])
        elif edge[1] == node:
            n.append(edge[0])
    return n

def f(u, v):
    s = (u, v)
    if s in edges:
        return edges[s]
    if s[::-1] in edges:
        return edges[s[::-1]]

path = [SOURCE] # Circuit of nodes
fT = 0 # Total fuel consumed
T = None # Target/Destination
while len(path) <= len(nodes):

    print(T, path[-1])
    if path[-1] == T:
        break

    T = path[-1]

    # Iteratively find smallest edge not already in the circuit.

    fmin = float('inf')
    Tmin = None

    for v in neighbours(T):

        if v in path: continue

        aux = f(T, v)
        rem = 0
        if v != SOURCE:
            rem = f(v, SOURCE)

        if fT + aux + rem > F: continue

        if aux >= fmin: continue

        fmin = aux
        Tmin = v

    # Add closest (unvisited) neighbour to circuit and add the weight to the total fuel consumed.

    if Tmin is not None:
        path.append(Tmin)
        fT += fmin

# Complete the circuit by appending the source node 
path.append(SOURCE)
fT += f(path[-2], path[-1])

print(" - ".join(path))
print(f"Total Fuel Consumed: {fT}")