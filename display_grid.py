from matrix import Matrix
from os.path import join, dirname

if __name__ == "__main__":

    grid = Matrix(55, 40)
    grid.zero_cell_placeholder = "0"

    with open(join(dirname(__file__), "locations.txt"), "r") as f:
        locations = f.read()

    for location in locations.split("\n"):

        s = location.split()
        if len(s) < 2: continue

        pair = [int(s[0][:-1]), int(s[1])]
        name = " ".join(s[2:])
        
        grid[*pair] = name

    print(grid)

