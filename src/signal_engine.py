import matplotlib.pyplot as plt
import time


class SignalEngine:

    def __init__(
        self,
        visual_mode="3D"
    ):

        self.visual_mode = visual_mode

        self.fig, self.ax = plt.subplots()

        plt.ion()


    # -------------------------
    # CLEAR CANVAS
    # -------------------------
    def clear_canvas(self):

        self.ax.clear()

        self.ax.set_title(
            "FPGA Timing-Aware Routing"
        )

        self.ax.axis("off")


        # -------------------------
        # LOCK VIEWPORT
        # -------------------------
        self.ax.set_xlim(-1, 4)

        self.ax.set_ylim(-7, 1)


    # -------------------------
    # DRAW FPGA
    # -------------------------
    def draw_fpga(
        self,
        fabric,
        routing,
        switchbox,
        lut_labels=None,
        active_lut=None
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


            if lut_name == active_lut:

                color = "yellow"

                size = 4000

            else:

                color = "skyblue"

                size = 3000


            self.ax.scatter(
                x,
                y,
                s=size,
                color=color,
                edgecolors="black",
                zorder=3
            )


            if (
                lut_labels and
                lut_name in lut_labels
            ):

                text = (

                    lut_name +
                    "\n(" +
                    lut_labels[lut_name] +
                    ")"
                )

            else:

                text = lut_name


            self.ax.text(
                x,
                y,
                text,
                ha='center',
                va='center',
                fontsize=8,
                fontweight='bold',
                zorder=4
            )


        # -------------------------
        # DRAW ROUTES
        # -------------------------
        for source, neighbors in routing.graph.items():

            for destination in neighbors:

                source_position = fabric.get_position(
                    source
                )

                destination_position = fabric.get_position(
                    destination
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
                        source +
                        "->" +
                        destination
                    )


                    delay = routing.route_delays[
                        route_name
                    ]


                    # -------------------------
                    # DELAY COLOR
                    # -------------------------
                    if delay == 1:

                        route_color = "lime"

                    elif delay == 2:

                        route_color = "orange"

                    else:

                        route_color = "red"


                    self.ax.plot(
                        [x1, x2],
                        [y1, y2],
                        color=route_color,
                        linewidth=3,
                        zorder=1
                    )


                    # -------------------------
                    # DELAY LABEL
                    # -------------------------
                    delay_x = (
                        x1 + x2
                    ) / 2

                    delay_y = (
                        y1 + y2
                    ) / 2


                    self.ax.text(
                        delay_x,
                        delay_y,
                        str(delay),
                        fontsize=10,
                        fontweight='bold',
                        color="black",
                        zorder=5
                    )


                    # -------------------------
                    # VIA
                    # -------------------------
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
                            s=250,
                            color="purple",
                            edgecolors="black",
                            zorder=2
                        )


        # -------------------------
        # DRAW SIGNAL PACKETS
        # -------------------------
        for packet in routing.signal_queue:

            source_position = fabric.get_position(
                packet["source"]
            )

            destination_position = fabric.get_position(
                packet["destination"]
            )


            if (
                not source_position or
                not destination_position
            ):

                continue


            s_layer, s_row, s_col = source_position

            d_layer, d_row, d_col = destination_position


            x1 = s_col + (s_layer * 0.3)

            y1 = -s_row + (s_layer * 0.3)

            x2 = d_col + (d_layer * 0.3)

            y2 = -d_row + (d_layer * 0.3)


            # -------------------------
            # CLAMP PROGRESS
            # -------------------------
            t = min(
                packet["progress"],
                1.0
            )


            signal_x = x1 + (x2 - x1) * t

            signal_y = y1 + (y2 - y1) * t


            self.ax.scatter(
                signal_x,
                signal_y,
                s=300,
                color="lime",
                edgecolors="black",
                zorder=6
            )


        self.fig.canvas.draw()

        self.fig.canvas.flush_events()


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

            plt.pause(0.05)


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