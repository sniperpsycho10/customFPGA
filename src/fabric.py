class Fabric:

    def __init__(self):

        self.luts = {}

        self.grid = {}


    def add_lut(
        self,
        lut,
        layer,
        row,
        column
    ):

        self.luts[lut.name] = lut

        self.grid[
            (layer, row, column)
        ] = lut.name


    def get_position(
        self,
        lut_name
    ):

        for position, name in self.grid.items():

            if name == lut_name:

                return position

        return None


    def show_grid(self):

        print("\nFPGA Layered Grid:\n")

        for position, lut_name in self.grid.items():

            print(
                lut_name,
                "->",
                position
            )