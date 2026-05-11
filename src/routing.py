class Routing:

    def __init__(self):
        self.routes = {}


    def add_route(self, source, destination):

        if source not in self.routes:
            self.routes[source] = []

        self.routes[source].append(destination)


    def show_routes(self):

        for source, destinations in self.routes.items():

            for destination in destinations:
                print(source, "->", destination)


    def route_signal(
        self,
        source,
        signal,
        fabric,
        switchbox
    ):

        destinations = self.routes[source]

        # Find source LUT position
        source_lut = source.replace("_OUT", "")

        source_position = None

        for position, lut_name in fabric.grid.items():

            if lut_name == source_lut:
                source_position = position

        for destination_lut_name, destination_index in destinations:

            route_name = source + "->" + destination_lut_name

            # Check switch enabled
            if switchbox.is_enabled(route_name):

                # Check neighbor relationship
                neighbors = fabric.get_neighbors(
                    source_position[0],
                    source_position[1]
                )

                if destination_lut_name in neighbors:

                    destination_lut = fabric.luts[
                        destination_lut_name
                    ]

                    destination_lut.inputs[
                        destination_index
                    ] = signal

                    print(
                        "Neighbor Route Success:",
                        route_name
                    )

                else:

                    print(
                        "Route Failed (Not Neighbor):",
                        route_name
                    )

            else:

                print(
                    "Route Blocked:",
                    route_name
                )