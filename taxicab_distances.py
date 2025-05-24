"""

For U3O3 SAT. Part1.
To calculate the 'taxi-cab' or 'Manhattan' distance between towns (non-zero entries) in the map matrix.

"""


from matrix import Matrix
from os.path import join, dirname

def generate_nodes(filename: str = "locations.txt") -> list[str]:
    
    with open(join(dirname(__file__), filename), "r") as f:
        locations_string = f.read()

    names: list[str] = []

    for location in locations_string.split("\n"):
        s = location.split()
        if len(s) < 2: continue

        name = " ".join(s[2:])
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
        name = " ".join(s[2:])
        
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

            edges[(start, dest)] = taxicab_distance

    return edges

if __name__ == "__main__":

    print("Nodes:")
    print(generate_nodes())
    print("Edges:")
    print(generate_edges())