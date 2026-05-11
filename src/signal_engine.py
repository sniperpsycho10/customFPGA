import matplotlib.pyplot as plt


class SignalEngine:

    def draw_fpga(self, fabric, routing):

        fig, ax = plt.subplots()

        # Draw LUTs
        for (row, column), lut_name in fabric.grid.items():

            ax.scatter(column, -row, s=3000)

            ax.text(
                column,
                -row,
                lut_name,
                ha='center',
                va='center',
                fontsize=10
            )

        # Draw Routing Lines
        for source, destinations in routing.routes.items():

            source_lut = source.replace("_OUT", "")

            source_position = None

            # Find source LUT position
            for position, lut_name in fabric.grid.items():

                if lut_name == source_lut:
                    source_position = position

            for destination_lut, _ in destinations:

                destination_position = None

                # Find destination LUT position
                for position, lut_name in fabric.grid.items():

                    if lut_name == destination_lut:
                        destination_position = position

                # Draw line
                if source_position and destination_position:

                    x1 = source_position[1]
                    y1 = -source_position[0]

                    x2 = destination_position[1]
                    y2 = -destination_position[0]

                    ax.plot([x1, x2], [y1, y2])

        ax.set_title("FPGA Grid Visualization")

        plt.show()