import matplotlib.pyplot as plt
import time
import numpy as np


class SignalEngine:

    def __init__(self):

        self.signal_queue = []


    def add_signal_event(
        self,
        source,
        signal
    ):

        self.signal_queue.append(
            (source, signal)
        )


    def process_signal_queue(
        self,
        routing,
        fabric,
        switchbox
    ):

        active_routes = []

        while self.signal_queue:

            source, signal = self.signal_queue.pop(0)

            routed_paths = routing.route_signal(
                source,
                signal,
                fabric,
                switchbox
            )

            active_routes.extend(routed_paths)

        return active_routes


    def animate_signal(
        self,
        fabric,
        source_lut,
        destination_lut,
        lut_labels=None
    ):

        plt.clf()

        fig = plt.gcf()
        ax = fig.gca()


        # Draw LUTs
        for (row, column), lut_name in fabric.grid.items():

            ax.scatter(
                column,
                -row,
                s=3000
            )

            # Display labels
            if lut_labels and lut_name in lut_labels:

                display_text = (
                    lut_name +
                    "\n(" +
                    lut_labels[lut_name] +
                    ")"
                )

            else:

                display_text = lut_name


            ax.text(
                column,
                -row,
                display_text,
                ha='center',
                va='center',
                fontsize=10
            )


        # Find positions
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


        # Draw wire
        ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=2
        )


        # Animate moving signal
        steps = 30

        for t in np.linspace(0, 1, steps):

            signal_x = x1 + (x2 - x1) * t
            signal_y = y1 + (y2 - y1) * t

            dot = ax.scatter(
                signal_x,
                signal_y,
                s=300
            )

            plt.pause(0.05)

            dot.remove()


        plt.draw()


    def animate_lut_activation(
        self,
        fabric,
        active_lut,
        lut_labels=None
    ):

        plt.clf()

        fig = plt.gcf()
        ax = fig.gca()


        pulse_sizes = [
            3000,
            4500,
            6000,
            4500,
            3000
        ]


        for size in pulse_sizes:

            plt.clf()

            ax = plt.gca()

            for (row, column), lut_name in fabric.grid.items():

                if lut_name == active_lut:

                    ax.scatter(
                        column,
                        -row,
                        s=size
                    )

                else:

                    ax.scatter(
                        column,
                        -row,
                        s=3000
                    )


                # Display labels
                if lut_labels and lut_name in lut_labels:

                    display_text = (
                        lut_name +
                        "\n(" +
                        lut_labels[lut_name] +
                        ")"
                    )

                else:

                    display_text = lut_name


                ax.text(
                    column,
                    -row,
                    display_text,
                    ha='center',
                    va='center',
                    fontsize=10
                )

            ax.set_title(
                "LUT Activation"
            )

            plt.pause(0.2)


    def draw_fpga(
        self,
        fabric,
        lut_labels=None
    ):

        plt.clf()

        fig = plt.gcf()
        ax = fig.gca()


        for (row, column), lut_name in fabric.grid.items():

            ax.scatter(
                column,
                -row,
                s=3000
            )


            # Display logic labels
            if lut_labels and lut_name in lut_labels:

                display_text = (
                    lut_name +
                    "\n(" +
                    lut_labels[lut_name] +
                    ")"
                )

            else:

                display_text = lut_name


            ax.text(
                column,
                -row,
                display_text,
                ha='center',
                va='center',
                fontsize=10
            )

        ax.set_title(
            "FPGA Configuration Visualization"
        )

        plt.draw()


    def run_cycle(
        self,
        cycle_number
    ):

        print("\n==========")
        print("Cycle", cycle_number)
        print("==========")

        time.sleep(1)