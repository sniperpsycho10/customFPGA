import random
from collections import deque


class Routing:

    def __init__(self):

        self.graph = {}

        self.congestion = {}

        self.signal_queue = {}

        self.signal_queue = []

        self.route_delays = {}

        self.critical_path = None

        self.max_delay = 0


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


        # -------------------------
        # RANDOM DELAY
        # -------------------------
        delay = random.randint(
            1,
            5
        )


        self.route_delays[
            route_name
        ] = delay


        # -------------------------
        # CRITICAL PATH TRACKING
        # -------------------------
        if delay > self.max_delay:

            self.max_delay = delay

            self.critical_path = route_name


    # -------------------------
    # SHOW GRAPH
    # -------------------------
    def show_graph(self):

        print(
            "\nFPGA Routing Graph:\n"
        )


        for source, destinations in self.graph.items():

            print(
                source,
                "->",
                destinations
            )


    # -------------------------
    # AUTO ROUTE
    # -------------------------
    def auto_route(
        self,
        source,
        destination
    ):

        queue = deque()

        queue.append(
            (source, [source])
        )

        visited = set()


        while queue:

            current, path = queue.popleft()


            if current == destination:

                print(
                    "\nAuto-Routed Path:"
                )

                print(path)

                return path


            visited.add(current)


            for neighbor in self.graph.get(
                current,
                []
            ):

                if neighbor not in visited:

                    queue.append(
                        (
                            neighbor,
                            path + [neighbor]
                        )
                    )


        return None


    # -------------------------
    # INJECT SIGNAL
    # -------------------------
    def inject_signal(
        self,
        source_output_name,
        signal_value,
        current_cycle
    ):

        source_lut = source_output_name.replace(
            "_OUT",
            ""
        )


        if source_lut not in self.graph:

            return


        for destination in self.graph[
            source_lut
        ]:

            route_name = (

                source_lut +
                "->" +
                destination
            )


            delay = self.route_delays[
                route_name
            ]


            packet = {

                "source": source_lut,

                "destination": destination,

                "signal": signal_value,

                "delay": delay,

                "progress": 0.0,

                "arrival_cycle": (
                    current_cycle + delay
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


            packet["progress"] += (

                1.0 / (delay * 5)
            )


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

            self.signal_queue.remove(
                packet
            )


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
                "/ 3"
            )


    # -------------------------
    # SHOW TIMING REPORT
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
    # SHOW CRITICAL PATH
    # -------------------------
    def show_critical_path(self):

        print(
            "\nCRITICAL PATH ANALYSIS:\n"
        )


        print(
            "Critical Route:",
            self.critical_path
        )


        print(
            "Worst Delay:",
            self.max_delay,
            "cycles"
        )


        estimated_frequency = (

            100 / self.max_delay
        )


        print(
            "Estimated Max Clock:",
            round(
                estimated_frequency,
                2
            ),
            "MHz"
        )