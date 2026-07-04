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
        self.ppc_w = self.maze_w_pxl / self.maze_w
        self.offset_h = (self.screen_h - self.maze_h_pxl) / 2
        self.offset_w = (self.screen_w - self.maze_w_pxl) / 2

    def maze_to_pxl(self, case: tuple[int, int]) -> tuple[int, int]:
        pxl_line = case[0] * self.ppc_w + self.offset_w
        pxl_col = case[1] * self.ppc_h + self.offset_h
        return (pxl_line, pxl_col)

    def pxl_to_maze(self, pxl: tuple[int, int]) -> tuple[int, int]:
        pxl_line = pxl[0]
        pxl_col = pxl[1]
        player_maze_x = (pxl_line - self.offset_w) // self.ppc_w
        player_maze_y = (pxl_col - self.offset_h) // self.ppc_h
        return (int(player_maze_x), int(player_maze_y))

    def get_offset_case(self, size_img: tuple[int, int], pxl_pos: tuple[float, float]) -> tuple[float, float]:
        mid_case_x = pxl_pos[0] + self.ppc_w // 2
        mid_case_y = pxl_pos[1] + self.ppc_h // 2
        offset_img_x = size_img[0] // 2
        offset_img_y = size_img[1] // 2
        result = (mid_case_y - offset_img_y, mid_case_x - offset_img_x)
        return result
