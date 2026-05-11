from collections import deque


class Routing:

    def __init__(self):

        self.routes = {}

        self.graph = {}

        self.congestion = {}

        self.max_capacity = 3


    # -------------------------
    # FPGA GRAPH CONNECTIONS
    # -------------------------
    def add_connection(
        self,
        source,
        destination
    ):

        if source not in self.graph:

            self.graph[source] = []


        self.graph[source].append(
            destination
        )


        # Initialize congestion
        route_name = (
            source +
            "->" +
            destination
        )

        self.congestion[
            route_name
        ] = 0


    # -------------------------
    # BFS PATHFINDING
    # -------------------------
    def find_path(
        self,
        start,
        end
    ):

        queue = deque()

        queue.append(
            (start, [start])
        )

        visited = set()


        while queue:

            current_node, path = queue.popleft()


            if current_node == end:

                return path


            visited.add(current_node)


            neighbors = self.graph.get(
                current_node,
                []
            )


            for neighbor in neighbors:

                if neighbor not in visited:

                    queue.append(
                        (
                            neighbor,
                            path + [neighbor]
                        )
                    )


        return None


    # -------------------------
    # AUTO ROUTE
    # -------------------------
    def auto_route(
        self,
        source,
        destination
    ):

        path = self.find_path(
            source,
            destination
        )


        if path:

            print(
                "\nAuto-Routed Path:"
            )

            print(path)


            # Create route list only once
            if (
                source + "_OUT"
                not in self.routes
            ):

                self.routes[
                    source + "_OUT"
                ] = []


            # Append route
            self.routes[
                source + "_OUT"
            ].append(
                (
                    destination,
                    0
                )
            )


            # Initialize logical congestion
            logical_route = (
                source +
                "->" +
                destination
            )


            if (
                logical_route
                not in self.congestion
            ):

                self.congestion[
                    logical_route
                ] = 0

        else:

            print(
                "\nNo valid route found."
            )


    # -------------------------
    # ROUTE SIGNAL
    # -------------------------
    def route_signal(
        self,
        source,
        signal,
        fabric,
        switchbox
    ):

        active_paths = []


        if source not in self.routes:

            return active_paths


        destinations = self.routes[source]


        for (
            destination_lut_name,
            destination_index
        ) in destinations:


            route_name = (
                source.replace(
                    "_OUT",
                    ""
                ) +
                "->" +
                destination_lut_name
            )


            # Check switch
            switch_route = (
                source +
                "->" +
                destination_lut_name
            )


            if not switchbox.is_enabled(
                switch_route
            ):

                print(
                    "Blocked Route:",
                    route_name
                )

                continue


            # Check congestion
            if self.congestion[
                route_name
            ] >= self.max_capacity:

                print(
                    "Congested Route:",
                    route_name
                )

                continue


            # Increment congestion
            self.congestion[
                route_name
            ] += 1


            # Route signal
            destination_lut = fabric.luts[
                destination_lut_name
            ]


            destination_lut.inputs[
                destination_index
            ] = signal


            print(
                "Signal Arrived:",
                route_name
            )


            active_paths.append(
                route_name
            )


        return active_paths


    # -------------------------
    # RESET CONGESTION
    # -------------------------
    def reset_congestion(self):

        for route in self.congestion:

            self.congestion[route] = 0


    # -------------------------
    # SHOW CONGESTION
    # -------------------------
    def show_congestion(self):

        print(
            "\nRouting Congestion:\n"
        )


        for route, usage in self.congestion.items():

            print(
                route,
                "->",
                usage,
                "/",
                self.max_capacity
            )


    # -------------------------
    # SHOW GRAPH
    # -------------------------
    def show_graph(self):

        print(
            "\nFPGA Routing Graph:\n"
        )


        for node, neighbors in self.graph.items():

            print(
                node,
                "->",
                neighbors
            )