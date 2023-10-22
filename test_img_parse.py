from sortpuz import img_parse
from sortpuz.models.base import ImgConfig
from sortpuz.plotting import plot_game

if __name__ == "__main__":
    img_cfg = ImgConfig(tube_count=(6, 5), num_colors=4)
    color_point_matrix = img_parse.get_color_map(img_cfg)

    color_matrix = img_parse.get_color_matrix(color_point_matrix)

    plot_game(color_matrix)