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
            "Advanced FPGA Architecture"
        )

        self.ax.axis("off")


    # -------------------------
    # ROUTE COLOR BY CONGESTION
    # -------------------------
    def get_route_color(
        self,
        usage,
        max_capacity,
        active=False,
        blocked=False
    ):

        if blocked:

            return "red"


        if active:

            return "lime"


        utilization = usage / max_capacity


        if utilization < 0.33:

            return "gray"

        elif utilization < 0.66:

            return "orange"

        else:

            return "magenta"


    # -------------------------
    # DRAW FPGA
    # -------------------------
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


        # -------------------------
        # DRAW LUTS
        # -------------------------
        for (
            layer,
            row,
            column
        ), lut_name in fabric.grid.items():

            x = column + (layer * 0.3)
            y = -row + (layer * 0.3)


            # Active LUT
            if lut_name == active_lut:

                lut_color = "yellow"
                size = 4000

            else:

                lut_color = "skyblue"
                size = 3000


            # Shadow
            self.ax.scatter(
                x + 0.05,
                y - 0.05,
                s=size,
                color="black",
                alpha=0.25
            )


            # Main LUT
            self.ax.scatter(
                x,
                y,
                s=size,
                color=lut_color,
                edgecolors="black"
            )


            # Labels
            if (
                lut_labels and
                lut_name in lut_labels
            ):

                display_text = (
                    lut_name +
                    "\n(" +
                    lut_labels[lut_name] +
                    ")\nL" +
                    str(layer)
                )

            else:

                display_text = lut_name


            self.ax.text(
                x,
                y,
                display_text,
                ha='center',
                va='center',
                fontsize=8,
                fontweight='bold'
            )


        # -------------------------
        # DRAW ROUTES
        # -------------------------
        for source, destinations in routing.routes.items():

            source_lut = source.replace(
                "_OUT",
                ""
            )

            source_position = fabric.get_position(
                source_lut
            )


            for destination_lut, _ in destinations:

                destination_position = fabric.get_position(
                    destination_lut
                )


                if (
                    source_position and
                    destination_position
                ):

                    s_layer, s_row, s_col = source_position

                    d_layer, d_row, d_col = destination_position


                    x1 = s_col + (s_layer * 0.3)
                    y1 = -s_row + (s_layer * 0.3)

                    x2 = d_col + (d_layer * 0.3)
                    y2 = -d_row + (d_layer * 0.3)


                    route_name = (
                        source_lut +
                        "->" +
                        destination_lut
                    )


                    usage = routing.congestion[
                        route_name
                    ]


                    blocked = not switchbox.is_enabled(
                        source +
                        "->" +
                        destination_lut
                    )


                    active = (
                        active_routes and
                        (
                            source +
                            "->" +
                            destination_lut
                        ) in active_routes
                    )


                    route_color = self.get_route_color(
                        usage,
                        routing.max_capacity,
                        active,
                        blocked
                    )


                    line_width = 2 + usage


                    # Route shadow
                    self.ax.plot(
                        [x1 + 0.03, x2 + 0.03],
                        [y1 - 0.03, y2 - 0.03],
                        color="black",
                        alpha=0.2,
                        linewidth=line_width + 1
                    )


                    # Main route
                    self.ax.plot(
                        [x1, x2],
                        [y1, y2],
                        color=route_color,
                        linewidth=line_width
                    )


                    # Via visualization
                    if s_layer != d_layer:

                        via_x = (
                            x1 + x2
                        ) / 2

                        via_y = (
                            y1 + y2
                        ) / 2


                        self.ax.scatter(
                            via_x,
                            via_y,
                            s=500,
                            color="orange",
                            edgecolors="black"
                        )


        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


    # -------------------------
    # ANIMATE SIGNAL
    # -------------------------
    def animate_signal(
        self,
        fabric,
        routing,
        switchbox,
        source_lut,
        destination_lut,
        lut_labels=None
    ):

        source_position = fabric.get_position(
            source_lut
        )

        destination_position = fabric.get_position(
            destination_lut
        )


        s_layer, s_row, s_col = source_position

        d_layer, d_row, d_col = destination_position


        x1 = s_col + (s_layer * 0.3)
        y1 = -s_row + (s_layer * 0.3)

        x2 = d_col + (d_layer * 0.3)
        y2 = -d_row + (d_layer * 0.3)


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


    # -------------------------
    # LUT ACTIVATION
    # -------------------------
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


    # -------------------------
    # RUN CYCLE
    # -------------------------
    def run_cycle(
        self,
        cycle_number
    ):

        print("\n==========")
        print("Cycle", cycle_number)
        print("==========")

        time.sleep(1)