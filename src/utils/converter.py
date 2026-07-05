from .. import constant


class Converter():
    def __init__(
            self,
            maze_size: tuple[int, int],
            maze_size_pxl: tuple[int, int],
            screen_size: tuple[int, int]
            ) -> None:
        self.maze_h = maze_size[0]
        self.maze_w = maze_size[1]
        self.maze_h_pxl = maze_size_pxl[0]
        self.maze_w_pxl = maze_size_pxl[1]
        self.screen_h = screen_size[0]
        self.screen_w = screen_size[1]
        self.ppc_h = self.maze_h_pxl / self.maze_h
        # self.ppc_h = self.maze_h_pxl - ((self.maze_h + 1) * constant.WALL_WIDTH) / self.maze_h
        self.ppc_w = self.maze_w_pxl / self.maze_w
        # self.ppc_w = self.maze_w_pxl - ((self.maze_w + 1) * constant.WALL_WIDTH) / self.maze_w
        self.offset_h = (self.screen_h - self.maze_h_pxl) / 2
        self.offset_w = (self.screen_w - self.maze_w_pxl) / 2

    def maze_to_pxl(self, case: tuple[int, int]) -> tuple[int, int]:
        pxl_y = case[0] * self.ppc_w + self.offset_w
        # pxl_y = case[0] * (self.ppc_w + constant.WALL_WIDTH) + self.offset_w
        pxl_x = case[1] * self.ppc_h + self.offset_h
        # pxl_x = case[1] * (self.ppc_h + constant.WALL_WIDTH) + self.offset_h
        return (pxl_x, pxl_y)

    def pxl_to_maze(self, pxl: tuple[int, int]) -> tuple[int, int]:
        pxl_x = pxl[0]
        pxl_y = pxl[1]
        player_maze_col = (pxl_x - self.offset_h) // self.ppc_h
        player_maze_line = (pxl_y - self.offset_w) // self.ppc_w
        return (int(player_maze_line), int(player_maze_col))

    def get_coord_sprite(self, size_img: tuple[int, int], pxl_pos: tuple[float, float]) -> tuple[float, float]:
        mid_case_x = pxl_pos[0] + self.ppc_h // 2
        mid_case_y = pxl_pos[1] + self.ppc_w // 2
        offset_img_x = size_img[0] // 2
        offset_img_y = size_img[1] // 2
        x = constant.WALL_WIDTH / 2 + mid_case_x - offset_img_x
        y = constant.WALL_WIDTH / 2 + mid_case_y - offset_img_y
        result = (x, y)
        return result



# if __name__ == "__main__":
#     conv = Converter((9, 9), (360, 360), (1920, 1080))
#     maze = (1, 0)
#     pxl = conv.maze_to_pxl(maze)
#     print(pxl)
#     maze = conv.pxl_to_maze(pxl)
#     print(maze)