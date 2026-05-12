import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time


class SignalEngine:

    def __init__(self):

        plt.ion()

        self.fig = plt.figure(
            figsize=(12, 9)
        )

        self.ax = self.fig.add_subplot(
            111,
            projection='3d'
        )

        # -------------------------
        # INTERACTIVE CONTROLS
        # -------------------------
        self.fig.canvas.toolbar_visible = True


    # -------------------------
    # CLEAR
    # -------------------------
    def clear_canvas(self):

        self.ax.cla()

        self.ax.set_title(
            "Interactive 3D FPGA Floorplanner"
        )

        self.ax.set_xlim(0, 10)

        self.ax.set_ylim(0, 10)

        self.ax.set_zlim(0, 5)

        self.ax.set_xlabel("X")

        self.ax.set_ylabel("Y")

        self.ax.set_zlabel("Layer")


        # -------------------------
        # BETTER VIEW
        # -------------------------
        self.ax.view_init(
            elev=28,
            azim=35
        )


        # -------------------------
        # CLEANER LOOK
        # -------------------------
        self.ax.grid(True)

        self.ax.set_box_aspect(
            [1, 1, 0.6]
        )


    # -------------------------
    # DRAW FPGA
    # -------------------------
    def draw_fpga(
        self,
        fabric,
        routing,
        switchbox,
        lut_labels=None,
        active_component=None
    ):

        self.clear_canvas()


        # ==================================================
        # FPGA TILE GRID
        # ==================================================

        grid_x = []
        grid_y = []
        grid_z = []


        for x in range(10):

            for y in range(10):

                grid_x.append(x)

                grid_y.append(y)

                grid_z.append(0)


        self.ax.scatter(

            grid_x,
            grid_y,
            grid_z,

            color='gray',

            alpha=0.12,

            s=12
        )


        # ==================================================
        # COMPONENTS
        # ==================================================

        for component, position in fabric.floorplan.items():

            x, y = position


            # -------------------------
            # LUT
            # -------------------------
            if component.startswith(
                "LUT"
            ):

                z = 1

                color = "deepskyblue"

                size = 600


            # -------------------------
            # REGISTER
            # -------------------------
            else:

                z = 2

                color = "purple"

                size = 400


            # -------------------------
            # ACTIVE
            # -------------------------
            if component == active_component:

                color = "yellow"

                size = 900


            # -------------------------
            # MAIN BLOCK
            # -------------------------
            self.ax.scatter(

                x,
                y,
                z,

                color=color,

                s=size,

                edgecolors='black'
            )


            # -------------------------
            # LABEL
            # -------------------------
            self.ax.text(

                x,
                y,
                z + 0.2,

                component,

                fontsize=8,

                fontweight='bold'
            )


        # ==================================================
        # ROUTING
        # ==================================================

        for source, neighbors in routing.graph.items():

            for destination in neighbors:

                source_pos = fabric.get_position(
                    source
                )

                dest_pos = fabric.get_position(
                    destination
                )


                if (
                    not source_pos or
                    not dest_pos
                ):

                    continue


                x1, y1 = source_pos

                x2, y2 = dest_pos


                z = 4


                route_name = (

                    source +
                    "->" +
                    destination
                )


                delay = routing.route_delays[
                    route_name
                ]


                # -------------------------
                # CRITICAL PATH
                # -------------------------
                if (
                    route_name ==
                    routing.critical_path
                ):

                    color = "magenta"

                    width = 5

                else:

                    if delay <= 2:

                        color = "lime"

                    elif delay <= 4:

                        color = "orange"

                    else:

                        color = "red"


                    width = 2


                # ==================================================
                # MANHATTAN ROUTING
                # ==================================================

                self.ax.plot(

                    [x1, x2],
                    [y1, y1],
                    [z, z],

                    color=color,

                    linewidth=width,

                    alpha=0.9
                )


                self.ax.plot(

                    [x2, x2],
                    [y1, y2],
                    [z, z],

                    color=color,

                    linewidth=width,

                    alpha=0.9
                )


                # -------------------------
                # DELAY LABEL
                # -------------------------
                mx = (x1 + x2) / 2

                my = (y1 + y2) / 2


                self.ax.text(

                    mx,
                    my,
                    z + 0.15,

                    str(delay),

                    fontsize=8
                )


        # ==================================================
        # SIGNAL PACKETS
        # ==================================================

        for packet in routing.signal_queue:

            source_pos = fabric.get_position(
                packet["source"]
            )

            dest_pos = fabric.get_position(
                packet["destination"]
            )


            if (
                not source_pos or
                not dest_pos
            ):

                continue


            x1, y1 = source_pos

            x2, y2 = dest_pos


            z = 4


            t = min(
                packet["progress"],
                1.0
            )


            # ==================================================
            # MANHATTAN PACKET MOTION
            # ==================================================

            if t < 0.5:

                local_t = t / 0.5

                signal_x = x1 + (
                    (x2 - x1) * local_t
                )

                signal_y = y1

            else:

                local_t = (
                    t - 0.5
                ) / 0.5


                signal_x = x2

                signal_y = y1 + (
                    (y2 - y1) * local_t
                )


            # -------------------------
            # GLOW
            # -------------------------
            self.ax.scatter(

                signal_x,
                signal_y,
                z,

                color='lightgreen',

                s=450,

                alpha=0.22
            )


            # -------------------------
            # CORE
            # -------------------------
            self.ax.scatter(

                signal_x,
                signal_y,
                z,

                color='lime',

                s=120,

                edgecolors='black'
            )


        # ==================================================
        # REFRESH
        # ==================================================

        self.fig.canvas.draw_idle()

        plt.pause(0.001)


    # -------------------------
    # CLOCK WAVE
    # -------------------------
    def animate_clock_wave(
        self,
        fabric,
        routing,
        switchbox,
        lut_labels
    ):

        print(
            "\nCLOCK WAVE PROPAGATING"
        )


        for flash in range(2):

            self.draw_fpga(

                fabric,
                routing,
                switchbox,
                lut_labels
            )


            for component, position in fabric.floorplan.items():

                if component.startswith(
                    "REG"
                ):

                    x, y = position


                    self.ax.scatter(

                        x,
                        y,
                        2.5,

                        color='yellow',

                        s=900,

                        alpha=0.35
                    )


            self.fig.canvas.draw_idle()

            plt.pause(0.08)


    # -------------------------
    # PIPELINE STAGE
    # -------------------------
    def show_pipeline_barrier(
        self,
        stage
    ):

        print(
            "\n=== PIPELINE STAGE",
            stage,
            "==="
        )


    # -------------------------
    # RUN CYCLE
    # -------------------------
    def run_cycle(
        self,
        cycle_number
    ):

        print("\n==========")

        print(
            "Pipeline Clock Cycle",
            cycle_number
        )

        print("==========")

        time.sleep(0.6)