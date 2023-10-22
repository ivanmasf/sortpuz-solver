"""
Take an image and turn it into Python objects representing the game using simple pixel parsing rules.
"""

from pathlib import Path
import tomllib
from typing import Literal, TypedDict, Unpack

import cv2
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np
from pydantic import BaseModel, model_validator

CWD = Path(__file__).parent

# Game 2 = Level 470
img = cv2.imread(str(CWD / "game2.jpeg"))


# Load the TOML configuration
with open(CWD / "config/color_parsing.toml", "r") as file:
    config = tomllib.loads(file.read())

# Extract the data
X_COORD = {int(k): tuple(v) for k, v in config["X_COORD"].items()}
Y_COORD = tuple(config["Y_COORD"]["values"])
Y_COORD_DELTA = {int(k): v for k, v in config["Y_COORD_DELTA"].items()}
RGB_INTERVAL = config['RGB_INTERVAL']


class RGB(TypedDict):
    R: int
    G: int
    B: int


NAME_RGB = {
    "Red": RGB(R=216, G=82, B=81),
    "Light Green": RGB(R=73, G=208, B=103),
    "Light Blue": RGB(R=0, G=184, B=238),
    "Brown": RGB(R=157, G=113, B=86),
    "Orange": RGB(R=249, G=122, B=19),
    "Pink": RGB(R=242, G=135, B=239),
    "Beige": RGB(R=249, G=181, B=82),
    "Purple": RGB(R=156, G=87, B=193),
    "Yellow": RGB(R=255, G=244, B=92),
    "Empty": RGB(R=228, G=218, B=209),
}


class Point(BaseModel):
    x: int
    y: int


class TubePoints(list[Point]):
    pass


class TubeRow(list[TubePoints]):
    pass


class ColorPointMatrix(tuple[TubeRow, TubeRow]):
    """
    Point(x,y) = ColorPointMatrix[row_idx][tube_idx][color_idx]

    TubePoints(Point 0, Point 1,...) = ColorPointMatrix[row_idx][tube_idx]

    TubeRow(TubePoints 0, TubePoints 1,..) = ColorPointMatrix[row_idx]

    ColorPointMatrix(TubeRow 0, TubeRow 1)
    """

    @staticmethod
    def ndim():
        return 3


class Color(BaseModel):
    name: str = ""
    rgb: RGB = RGB(R=-1, G=-1, B=-1)

    def __init__(self, **kwargs: Unpack[RGB]):
        super().__init__(**kwargs)

        self.rgb = RGB(**kwargs)

        self.name = self.get_color_name(**self.rgb)

    @staticmethod
    def get_color_name(**kwargs: Unpack[RGB]) -> str:
        for color_name, rgb in NAME_RGB.items():
            if (
                kwargs["R"]
                in range(rgb["R"] - RGB_INTERVAL, rgb["R"] + RGB_INTERVAL + 1)
                and kwargs["G"]
                in range(rgb["G"] - RGB_INTERVAL, rgb["G"] + RGB_INTERVAL + 1)
                and kwargs["B"]
                in range(rgb["B"] - RGB_INTERVAL, rgb["B"] + RGB_INTERVAL + 1)
            ):
                return color_name
        return ""

    @property
    def R(self) -> int:
        return self.rgb["R"]

    @R.setter
    def R(self, value: int):
        self.rgb["R"] = value
        self.name = self.get_color_name(**self.rgb)

    @property
    def G(self) -> int:
        return self.rgb["G"]

    @G.setter
    def G(self, value: int):
        self.rgb["G"] = value
        self.name = self.get_color_name(**self.rgb)

    @property
    def B(self) -> int:
        return self.rgb["B"]

    @B.setter
    def B(self, value: int):
        self.rgb["B"] = value
        self.name = self.get_color_name(**self.rgb)


def get_name_color_tuple(name_rgb: tuple[str, RGB]) -> tuple[str, Color]:
    return name_rgb[0], Color(**name_rgb[1])


COLORS = dict(map(get_name_color_tuple, NAME_RGB.items()))

for name, rgb in NAME_RGB.items():
    globals()[name.upper()] = Color(**rgb)

RED = COLORS["Red"]
LIGHT_GREEN = COLORS["Light Green"]
LIGHT_BLUE = COLORS["Light Blue"]


def get_point_color(pixel_coordinates: Point) -> Color:
    color_bgr = img[pixel_coordinates.y][pixel_coordinates.x]
    return Color(R=color_bgr[2], G=color_bgr[1], B=color_bgr[0])


def show_color(color: Color) -> None:
    # Create an image of size 10x10 with the specified color
    image = np.ones((10, 10, 3), dtype=np.uint8)
    image[:, :] = [color.R, color.G, color.B]

    # Set figure size to display the image at its original size (10x10 pixels)
    plt.figure(figsize=(10, 10), dpi=10)  # type:ignore

    # Display the image using matplotlib
    plt.imshow(image)  # type:ignore
    plt.axis("off")  # type:ignore
    plt.show()  # type:ignore


class ImgConfigInput(TypedDict):
    tube_count: tuple[
        Literal[5] | Literal[6],
        Literal[5] | Literal[6],
    ]
    num_colors: Literal[4] | Literal[5]
    color_point_matrix: ColorPointMatrix


class ImgConfig(BaseModel):
    tube_count: tuple[
        Literal[5] | Literal[6],
        Literal[5] | Literal[6],
    ]
    num_colors: Literal[4] | Literal[5]
    color_point_matrix: ColorPointMatrix = ColorPointMatrix()

    class Config:
        arbitrary_types_allowed = True

    @model_validator(mode="before")
    def set_color_map(cls, data: ImgConfigInput) -> ImgConfigInput:
        tube_count = data.get("tube_count")
        num_colors = data.get("num_colors")

        if tube_count and num_colors:
            constructed_map = (
                TubeRow(
                    [
                        TubePoints(
                            [
                                Point(x=x, y=Y_COORD[0] + i * Y_COORD_DELTA[num_colors])
                                for i in range(num_colors)
                            ]
                        )
                        for x in X_COORD[tube_count[0]]
                    ]
                ),
                TubeRow(
                    [
                        TubePoints(
                            [
                                Point(x=x, y=Y_COORD[1] + i * Y_COORD_DELTA[num_colors])
                                for i in range(num_colors)
                            ]
                        )
                        for x in X_COORD[tube_count[1]]
                    ]
                ),
            )

            data["color_point_matrix"] = ColorPointMatrix(constructed_map)

        return data


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


if __name__ == "__main__":
    img_cfg = ImgConfig(tube_count=(6, 5), num_colors=4)

    color_matrix: list[list[list[Color]]] = []
    for row in img_cfg.color_point_matrix:
        row_tubes: list[list[Color]] = []
        for tube in row:
            tube_colors: list[Color] = []
            for i, point in enumerate(tube):
                color = get_point_color(point)
                tube_colors.append(color)
                # print(f"point: {point} color: {color!r}")
            row_tubes.append(tube_colors)
        color_matrix.append(row_tubes)

    # for row_tubes in color_matrix:
    #     for tube_colors in row_tubes:
    #         for color in tube_colors:
    #             print(color,end='\n\n')
    #             show_color(color)

    plot_game(color_matrix)
