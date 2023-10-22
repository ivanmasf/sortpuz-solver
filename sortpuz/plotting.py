import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from sortpuz.models.color import Color


def plot_color(ax: Axes, color: Color):
    # Create an image of size 10x10 with the specified color
    image = np.ones((10, 10, 3), dtype=np.uint8)
    image[:, :] = [color.R, color.G, color.B]

    # Display the image using the axis object passed to the function
    ax.imshow(image)  # type: ignore
    ax.axis("off")


def plot_game(color_matrix: list[list[list[Color]]], single_figure: bool = True):
    # Determine the number of rows, tubes per row, and colors per tube
    num_rows = len(color_matrix)
    num_tubes = max(len(row) for row in color_matrix)
    num_colors = max(len(tube) for row in color_matrix for tube in row)

    if single_figure:
        # Create a figure for plotting
        fig = plt.figure(figsize=(10 * num_tubes, 10 * num_colors * num_rows))  # type: ignore

        # Loop through each color and plot it in the desired grid position
        for row_idx, row_tubes in enumerate(color_matrix):
            for tube_idx, tube_colors in enumerate(row_tubes):
                for color_idx, color in enumerate(tube_colors):
                    ax = fig.add_subplot(  # type: ignore
                        num_rows * num_colors,
                        num_tubes,
                        row_idx * num_colors * num_tubes
                        + tube_idx
                        + color_idx * num_tubes
                        + 1,
                    )
                    plot_color(ax, color)

        plt.tight_layout()
        plt.subplots_adjust(
            left=0.026, right=0.936, top=0.898, bottom=0.086, hspace=0.171, wspace=0.114
        )
        plt.show()  # type: ignore

    else:
        # Loop through each row in color_matrix
        for row_tubes in color_matrix:
            # Create a new figure for each row with adjusted size
            fig = plt.figure(figsize=(num_tubes, num_colors))  # type: ignore

            # Loop through each color and plot it in the desired grid position within the figure
            for tube_idx, tube_colors in enumerate(row_tubes):
                for color_idx, color in enumerate(tube_colors):
                    ax = fig.add_subplot(num_colors, num_tubes, tube_idx + color_idx * num_tubes + 1)  # type: ignore
                    plot_color(ax, color)

            plt.tight_layout()
            plt.show()  # type: ignore
