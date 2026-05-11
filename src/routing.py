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


    def route_signal(self, source, signal, luts, switchbox):

        destinations = self.routes[source]

        for destination_lut_name, destination_index in destinations:

            # Create route identifier
            route_name = source + "->" + destination_lut_name

            # Check switch state
            if switchbox.is_enabled(route_name):

                # Get LUT object
                destination_lut = luts[destination_lut_name]

                # Inject signal
                destination_lut.inputs[destination_index] = signal

                print("Signal Routed Through:", route_name)

            else:

                print("Route Blocked:", route_name)