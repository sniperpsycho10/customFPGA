class Routing:

    def __init__(self):
        self.routes = {}


    def add_route(self, source, destination):

        # Create list if source doesn't exist
        if source not in self.routes:
            self.routes[source] = []

        # Add destination to route list
        self.routes[source].append(destination)


    def show_routes(self):

        for source, destinations in self.routes.items():

            for destination in destinations:
                print(source, "->", destination)


    def route_signal(self, source, signal, luts):

        # Get all destinations
        destinations = self.routes[source]

        # Route signal to every destination
        for destination_lut_name, destination_index in destinations:

            # Get LUT object
            destination_lut = luts[destination_lut_name]

            # Inject signal
            destination_lut.inputs[destination_index] = signal