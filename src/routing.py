from collections import deque
import random


class Routing:

    def __init__(self):

        self.routes = {}

        self.graph = {}

        self.congestion = {}

        self.route_delays = {}

        self.max_capacity = 3

        self.signal_queue = []


    # -------------------------
    # ADD CONNECTION
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


        route_name = (
            source +
            "->" +
            destination
        )


        self.congestion[
            route_name
        ] = 0


        # Random timing delay
        self.route_delays[
            route_name
        ] = random.randint(1,3)


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


            visited.add(
                current_node
            )


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


            if (
                source + "_OUT"
                not in self.routes
            ):

                self.routes[
                    source + "_OUT"
                ] = []


            self.routes[
                source + "_OUT"
            ].append(
                (
                    destination,
                    0
                )
            )


    # -------------------------
    # INJECT SIGNAL
    # -------------------------
    def inject_signal(
        self,
        source,
        signal,
        current_cycle
    ):

        if source not in self.routes:

            return


        destinations = self.routes[source]


        for (
            destination_lut,
            destination_index
        ) in destinations:


            route_name = (

                source.replace(
                    "_OUT",
                    ""
                ) +

                "->" +

                destination_lut
            )


            delay = self.route_delays[
                route_name
            ]


            packet = {

                "source": source.replace(
                    "_OUT",
                    ""
                ),

                "destination": destination_lut,

                "signal": signal,

                "progress": 0.0,

                "delay": delay,

                "start_cycle": current_cycle,

                "arrival_cycle": (
                    current_cycle +
                    delay
                )
            }


            self.signal_queue.append(
                packet
            )


            print(
                "Injected Packet:",
                route_name,
                "| Delay =",
                delay
            )


       # -------------------------
    # ADVANCE SIGNALS
    # -------------------------
    def advance_signals(
        self,
        fabric,
        switchbox,
        current_cycle
    ):

        delivered_packets = []


        for packet in self.signal_queue:

            delay = packet["delay"]


            # -------------------------
            # SAFE PROGRESS UPDATE
            # -------------------------
            packet["progress"] += (

                1.0 / (delay * 5)
            )


            # Clamp
            if packet["progress"] > 1.0:

                packet["progress"] = 1.0


            if (
                current_cycle >=
                packet["arrival_cycle"]
            ):

                source = packet["source"]

                destination = packet[
                    "destination"
                ]


                route_name = (
                    source +
                    "->" +
                    destination
                )


                switch_name = (
                    source +
                    "_OUT->" +
                    destination
                )


                if switchbox.is_enabled(
                    switch_name
                ):

                    self.congestion[
                        route_name
                    ] += 1


                    destination_lut = fabric.luts[
                        destination
                    ]


                    destination_lut.inputs[
                        0
                    ] = packet["signal"]


                    print(
                        "Signal Arrived:",
                        route_name,
                        "| Arrival Cycle =",
                        current_cycle
                    )


                delivered_packets.append(
                    packet
                )


        for packet in delivered_packets:

            if packet in self.signal_queue:

                self.signal_queue.remove(
                    packet
                )


    # -------------------------
    # SHOW TIMING
    # -------------------------
    def show_timing_report(self):

        print(
            "\nFPGA Timing Report:\n"
        )


        for route, delay in self.route_delays.items():

            print(
                route,
                "->",
                delay,
                "cycle delay"
            )


    # -------------------------
    # RESET CONGESTION
    # -------------------------
    def reset_congestion(self):

        for route in self.congestion:

            self.congestion[
                route
            ] = 0


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