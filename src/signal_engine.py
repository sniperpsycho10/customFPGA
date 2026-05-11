import matplotlib.pyplot as plt
import time
import numpy as np


class SignalEngine:

    def __init__(
        self,
        visual_mode="3D"
    ):

        self.signal_queue = []

        self.visual_mode = visual_mode

        self.fig, self.ax = plt.subplots()

        plt.ion()


    def clear_canvas(self):

        self.ax.clear()

        self.ax.set_title(
            "Advanced FPGA Visualization"
        )

        self.ax.axis("off")


    def add_signal_event(
        self,
        source,
        signal
    ):

        self.signal_queue.append(
            (source, signal)
        )


    def draw_lut(
        self,
        x,
        y,
        lut_name,
        lut_color,
        size,
        label
    ):

        # --------------------
        # 3D MODE
        # --------------------
        if self.visual_mode == "3D":

            # Shadow layer
            self.ax.scatter(
                x + 0.05,
                y - 0.05,
                s=size,
                color="black",
                alpha=0.3
            )

            # Main LUT
            self.ax.scatter(
                x,
                y,
                s=size,
                color=lut_color,
                edgecolors="black"
            )

        # --------------------
        # 2D MODE
        # --------------------
        else:

            self.ax.scatter(
                x,
                y,
                s=size,
                color=lut_color,
                edgecolors="black"
            )


        self.ax.text(
            x,
            y,
            label,
            ha='center',
            va='center',
            fontsize=9,
            fontweight='bold'
        )


    def draw_route(
        self,
        x1,
        y1,
        x2,
        y2,
        color,
        width
    ):

        # --------------------
        # 3D ROUTING
        # --------------------
        if self.visual_mode == "3D":

            # Shadow route
            self.ax.plot(
                [x1 + 0.03, x2 + 0.03],
                [y1 - 0.03, y2 - 0.03],
                color="black",
                alpha=0.2,
                linewidth=width + 1
            )


        # Main route
        self.ax.plot(
            [x1, x2],
            [y1, y2],
            color=color,
            linewidth=width
        )


    def draw_fpga(
        self,
        fabric,
        routing,
        switchbox,
        lut_labels=None,
        active_lut=None,
        active_routes=None
    ):

        self.clear_canvas()


        # --------------------
        # DRAW LUTS
        # --------------------
        for (row, column), lut_name in fabric.grid.items():

            if lut_name == active_lut:

                lut_color = "yellow"
                size = 4000

            else:

                lut_color = "skyblue"
                size = 3000


            # Labels
            if (
                lut_labels and
                lut_name in lut_labels
            ):

                display_text = (
                    lut_name +
                    "\n(" +
                    lut_labels[lut_name] +
                    ")"
                )

            else:

                display_text = lut_name


            self.draw_lut(
                column,
                -row,
                lut_name,
                lut_color,
                size,
                display_text
            )


        # --------------------
        # DRAW ROUTES
        # --------------------
        for source, destinations in routing.routes.items():

            source_lut = source.replace(
                "_OUT",
                ""
            )

            source_position = None


            for position, lut_name in fabric.grid.items():

                if lut_name == source_lut:

                    source_position = position


            for destination_lut, _ in destinations:

                destination_position = None


                for position, lut_name in fabric.grid.items():

                    if lut_name == destination_lut:

                        destination_position = position


                if (
                    source_position and
                    destination_position
                ):

                    x1 = source_position[1]
                    y1 = -source_position[0]

                    x2 = destination_position[1]
                    y2 = -destination_position[0]


                    route_name = (
                        source +
                        "->" +
                        destination_lut
                    )


                    # Active route
                    if (
                        active_routes and
                        route_name in active_routes
                    ):

                        route_color = "lime"
                        line_width = 4


                    # Disabled route
                    elif not switchbox.is_enabled(
                        route_name
                    ):

                        route_color = "red"
                        line_width = 2


                    # Idle route
                    else:

                        route_color = "gray"
                        line_width = 2


                    self.draw_route(
                        x1,
                        y1,
                        x2,
                        y2,
                        route_color,
                        line_width
                    )


        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    def animate_signal(
        self,
        fabric,
        routing,
        switchbox,
        source_lut,
        destination_lut,
        lut_labels=None
    ):

        source_position = None
        destination_position = None


        for position, lut_name in fabric.grid.items():

            if lut_name == source_lut:

                source_position = position

            if lut_name == destination_lut:

                destination_position = position


        x1 = source_position[1]
        y1 = -source_position[0]

        x2 = destination_position[1]
        y2 = -destination_position[0]


        steps = 50


        for t in np.linspace(0, 1, steps):

            self.draw_fpga(
                fabric,
                routing,
                switchbox,
                lut_labels,
                active_routes=[
                    source_lut +
                    "_OUT->" +
                    destination_lut
                ]
            )


            signal_x = x1 + (x2 - x1) * t
            signal_y = y1 + (y2 - y1) * t


            self.ax.scatter(
                signal_x,
                signal_y,
                s=300,
                color="lime",
                edgecolors="black"
            )


            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

            plt.pause(0.02)


    def animate_lut_activation(
        self,
        fabric,
        routing,
        switchbox,
        active_lut,
        lut_labels=None
    ):

        pulse_sizes = [
            3000,
            4500,
            6000,
            4500,
            3000
        ]


        for size in pulse_sizes:

            self.draw_fpga(
                fabric,
                routing,
                switchbox,
                lut_labels,
                active_lut=active_lut
            )

            plt.pause(0.08)


    def run_cycle(
        self,
        cycle_number
    ):

        print("\n==========")
        print("Cycle", cycle_number)
        print("==========")

        time.sleep(1)