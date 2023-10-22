from typing import Unpack

from pydantic import BaseModel

from sortpuz.models.base import RGB
from sortpuz.constants.base_constants import NAME_RGB, RGB_INTERVAL

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