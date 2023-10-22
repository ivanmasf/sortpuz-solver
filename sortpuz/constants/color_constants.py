from sortpuz.models.base import RGB
from sortpuz.models.color import Color
from sortpuz.constants.base_constants import NAME_RGB


def get_name_color_tuple(name_rgb: tuple[str, RGB]) -> tuple[str, Color]:
    return name_rgb[0], Color(**name_rgb[1])


COLORS = dict(map(get_name_color_tuple, NAME_RGB.items()))

RED = COLORS["Red"]
LIGHT_GREEN = COLORS["Light Green"]
LIGHT_BLUE = COLORS["Light Blue"]
BROWN = COLORS["Brown"]
ORANGE = COLORS["Orange"]
PINK = COLORS["Pink"]
BEIGE = COLORS["Beige"]
PURPLE = COLORS["Purple"]
YELLOW = COLORS["Yellow"]
EMPTY = COLORS["Empty"]
