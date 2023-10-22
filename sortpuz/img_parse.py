"""
Take an image and turn it into Python objects representing the game using simple pixel parsing rules.
"""

from cv2.typing import MatLike

from sortpuz.constants.base_constants import (
    X_COORD,
    Y_COORD,
    Y_COORD_DELTA,
)
from sortpuz.models.base import Point, ColorPointMatrix, TubeRow, TubePoints, ImgConfig
from sortpuz.models.color import Color


def get_point_color(pixel_coordinates: Point, img: MatLike) -> Color:
    color_bgr = img[pixel_coordinates.y][pixel_coordinates.x]
    return Color(R=color_bgr[2], G=color_bgr[1], B=color_bgr[0])


def get_color_map(data: ImgConfig) -> ColorPointMatrix:
    tube_count = data.tube_count
    num_colors = data.num_colors

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

        return ColorPointMatrix(constructed_map)

    raise ValueError(
        f"Missing ImgConfig has zero tube_count {tube_count} or num_colors {num_colors}"
    )


def get_color_matrix(
    color_point_matrix: ColorPointMatrix, img: MatLike
) -> list[list[list[Color]]]:
    color_matrix: list[list[list[Color]]] = []
    for row in color_point_matrix:
        row_tubes: list[list[Color]] = []
        for tube in row:
            tube_colors: list[Color] = []
            for point in tube:
                color = get_point_color(point, img)
                tube_colors.append(color)
                # print(f"point: {point} color: {color!r}")
            row_tubes.append(tube_colors)
        color_matrix.append(row_tubes)

    return color_matrix
