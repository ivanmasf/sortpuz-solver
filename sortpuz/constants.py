import tomllib

from sortpuz.models.base import RGB

# Load the TOML configuration
with open("color_parsing.toml", "r") as file:
    config = tomllib.loads(file.read())

# Extract the data
X_COORD = {int(k): tuple(v) for k, v in config["X_COORD"].items()}
Y_COORD = tuple(config["Y_COORD"]["values"])
Y_COORD_DELTA = {int(k): v for k, v in config["Y_COORD_DELTA"].items()}
RGB_INTERVAL = config['RGB_INTERVAL']

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
