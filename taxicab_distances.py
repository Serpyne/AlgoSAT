"""

For U3O3 SAT. Part1.
To calculate the 'taxi-cab' or 'Manhattan' distance between towns (non-zero entries) in the map matrix.

"""


from matrix import Matrix
from os.path import join, dirname

def get_edge(edges, s):
    if s in edges:
        return edges[s]
    if s[::-1] in edges:
        return edges[s[::-1]]


def generate_nodes(filename: str = "locations.txt") -> list[str]:
    
    with open(join(dirname(__file__), filename), "r") as f:
        locations_string = f.read()

    names: list[str] = []

    for location in locations_string.split("\n"):
        s = location.split()
        if len(s) < 2: continue

        name = " ".join(s[2:-1])
        names.append(name)

    return names

def generate_edges(filename: str = "locations.txt") -> dict[tuple, int]:
    grid = Matrix(55, 40)
    grid.zero_cell_placeholder = ""

    with open(join(dirname(__file__), filename), "r") as f:
        locations_string = f.read()

    locations: dict[str, tuple] = {}
    names: list[str] = []

    for location in locations_string.split("\n"):

        s = location.split()
        if len(s) < 2: continue

        pair = [int(s[0][:-1]), int(s[1])]
        name = " ".join(s[2:-1])
        postcode = s[-1]
        
        grid[*pair] = name
        locations[name] = pair
        names.append(name)

    edges: dict[tuple: int] = {}

    for j in range(len(names)):
        for i in range(j + 1, len(names)):
            start = names[j]
            dest = names[i]
            x1, y1 = locations[start]
            x2, y2 = locations[dest]
            taxicab_distance = abs(x1 - x2) + abs(y1 - y2)

            edges[(start, dest)] = taxicab_distance * 36.5

    return edges

if __name__ == "__main__":

    print("Nodes:")
    print(generate_nodes())

    e = generate_edges()

    s = ["Exmouth", "Monkey Mia", "Broome", "Derby", "Esperance"]
    for x in s:
        u, v = ("Perth", x)
        print(f"Edge: {u, v}")
        print(get_edge(e, (u, v)))