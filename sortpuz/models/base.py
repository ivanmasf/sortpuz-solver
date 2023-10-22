from typing import TypedDict
from pydantic import BaseModel

class RGB(TypedDict):
    R: int
    G: int
    B: int

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


