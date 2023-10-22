import cv2

from sortpuz import img_parse
from sortpuz.models.base import ImgConfig
from sortpuz.plotting import plot_game

if __name__ == "__main__":
    # Game 2 = Level 470
    img = cv2.imread(str("game2.jpeg"))
    img_cfg = ImgConfig(tube_count=(6, 5), num_colors=4)
    color_point_matrix = img_parse.get_color_map(img_cfg)

    color_matrix = img_parse.get_color_matrix(color_point_matrix, img)

    plot_game(color_matrix)
