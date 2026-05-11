class Fabric:

    def __init__(self):

        self.luts = {}

        self.grid = {}


    def add_lut(self, lut, row, column):

        self.luts[lut.name] = lut

        self.grid[(row, column)] = lut.name


    def show_luts(self):

        for lut_name in self.luts:
            print(lut_name)


    def show_grid(self):

        print("\nFPGA Grid Layout:\n")

        for position, lut_name in self.grid.items():

            print(position, "->", lut_name)


    def get_neighbors(self, row, column):

        neighbors = []

        # Up
        if (row - 1, column) in self.grid:
            neighbors.append(
                self.grid[(row - 1, column)]
            )

        # Down
        if (row + 1, column) in self.grid:
            neighbors.append(
                self.grid[(row + 1, column)]
            )

        # Left
        if (row, column - 1) in self.grid:
            neighbors.append(
                self.grid[(row, column - 1)]
            )

        # Right
        if (row, column + 1) in self.grid:
            neighbors.append(
                self.grid[(row, column + 1)]
            )

        return neighbors