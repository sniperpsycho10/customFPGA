import random
import math


class Fabric:

    def __init__(self):

        # -------------------------
        # STORAGE
        # -------------------------
        self.luts = {}

        self.registers = {}

        self.floorplan = {}


        # -------------------------
        # CHIP SIZE
        # -------------------------
        self.width = 10

        self.height = 10


    # -------------------------
    # EMPTY TILE
    # -------------------------
    def find_empty_tile(self):

        while True:

            x = random.randint(
                1,
                self.width - 2
            )

            y = random.randint(
                1,
                self.height - 2
            )


            if (
                (x, y)
                not in self.floorplan.values()
            ):

                return x, y


    # -------------------------
    # ADD LUT
    # -------------------------
    def add_lut(
        self,
        lut
    ):

        self.luts[
            lut.name
        ] = lut


        x, y = self.find_empty_tile()


        self.floorplan[
            lut.name
        ] = [x, y]


    # -------------------------
    # ADD REGISTER
    # -------------------------
    def add_register(
        self,
        register,
        parent_lut_name=None
    ):

        self.registers[
            register.name
        ] = register


        if (
            parent_lut_name and
            parent_lut_name in self.floorplan
        ):

            lut_x, lut_y = self.floorplan[
                parent_lut_name
            ]


            nearby_tiles = [

                (lut_x + 1, lut_y),

                (lut_x - 1, lut_y),

                (lut_x, lut_y + 1),

                (lut_x, lut_y - 1)
            ]


            for tile in nearby_tiles:

                x, y = tile


                if (
                    x < 0 or
                    x >= self.width or
                    y < 0 or
                    y >= self.height
                ):

                    continue


                if (
                    tile
                    not in self.floorplan.values()
                ):

                    self.floorplan[
                        register.name
                    ] = [x, y]

                    return


        x, y = self.find_empty_tile()


        self.floorplan[
            register.name
        ] = [x, y]


    # -------------------------
    # FORCE-DIRECTED PLACEMENT
    # -------------------------
    def optimize_placement(
        self,
        netlist,
        iterations=80
    ):

        components = list(
            self.floorplan.keys()
        )


        for step in range(iterations):

            forces = {}


            # -------------------------
            # INIT FORCES
            # -------------------------
            for comp in components:

                forces[comp] = [0.0, 0.0]


            # ==================================================
            # REPULSION
            # ==================================================
            for a in components:

                for b in components:

                    if a == b:

                        continue


                    x1, y1 = self.floorplan[a]

                    x2, y2 = self.floorplan[b]


                    dx = x1 - x2

                    dy = y1 - y2


                    dist = math.sqrt(
                        dx*dx + dy*dy
                    ) + 0.01


                    repulsion = 0.08 / dist


                    forces[a][0] += (
                        dx / dist
                    ) * repulsion


                    forces[a][1] += (
                        dy / dist
                    ) * repulsion


            # ==================================================
            # ATTRACTION
            # ==================================================
            for source, destination in netlist.connections:

                if (
                    source not in self.floorplan or
                    destination not in self.floorplan
                ):

                    continue


                x1, y1 = self.floorplan[source]

                x2, y2 = self.floorplan[destination]


                dx = x2 - x1

                dy = y2 - y1


                dist = math.sqrt(
                    dx*dx + dy*dy
                ) + 0.01


                attraction = dist * 0.015


                forces[source][0] += (
                    dx / dist
                ) * attraction


                forces[source][1] += (
                    dy / dist
                ) * attraction


                forces[destination][0] -= (
                    dx / dist
                ) * attraction


                forces[destination][1] -= (
                    dy / dist
                ) * attraction


            # ==================================================
            # APPLY FORCES
            # ==================================================
            for comp in components:

                x, y = self.floorplan[comp]


                fx, fy = forces[comp]


                x += fx

                y += fy


                x = max(
                    1,
                    min(
                        self.width - 2,
                        x
                    )
                )

                y = max(
                    1,
                    min(
                        self.height - 2,
                        y
                    )
                )


                self.floorplan[comp] = [x, y]


    # -------------------------
    # SNAP TO GRID
    # -------------------------
    def snap_to_grid(self):

        occupied = set()


        for component in self.floorplan:

            x, y = self.floorplan[
                component
            ]


            gx = round(x)

            gy = round(y)


            while (
                (gx, gy)
                in occupied
            ):

                gx += 1


                if gx >= self.width:

                    gx = 1

                    gy += 1


            occupied.add(
                (gx, gy)
            )


            self.floorplan[
                component
            ] = [gx, gy]


    # -------------------------
    # GET POSITION
    # -------------------------
    def get_position(
        self,
        component_name
    ):

        position = self.floorplan.get(
            component_name
        )


        if not position:

            return None


        return (

            position[0],
            position[1]
        )


    # -------------------------
    # SHOW GRID
    # -------------------------
    def show_grid(self):

        print(
            "\nFPGA Floorplan:\n"
        )


        for component, position in self.floorplan.items():

            print(

                component,

                "-> Tile",

                (
                    round(position[0]),
                    round(position[1])
                )
            )


    # -------------------------
    # UTILIZATION
    # -------------------------
    def show_utilization(self):

        used_tiles = len(
            self.floorplan
        )

        total_tiles = (
            self.width *
            self.height
        )


        utilization = (
            used_tiles / total_tiles
        ) * 100


        print(
            "\nFPGA UTILIZATION REPORT:\n"
        )


        print(
            "Used Tiles:",
            used_tiles
        )


        print(
            "Total Tiles:",
            total_tiles
        )


        print(
            "Utilization:",
            round(
                utilization,
                2
            ),
            "%"
        )