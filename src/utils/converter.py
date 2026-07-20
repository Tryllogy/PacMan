from .. import constant


class Converter():
    def __init__(
            self,
            maze_size_cells: tuple[int, int],
            maze_size_pixels: tuple[int, int],
            screen_size: tuple[int, int]
            ) -> None:
        """Precompute cell sizes and centering offsets for the maze."""
        self.maze_rows = maze_size_cells[0]
        self.maze_cols = maze_size_cells[1]
        self.maze_height_px = maze_size_pixels[0]
        self.maze_width_px = maze_size_pixels[1]
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.cell_height_px = self.maze_height_px / self.maze_rows
        self.cell_width_px = self.maze_width_px / self.maze_cols
        self.offset_x = (self.screen_width - self.maze_width_px) / 2
        self.offset_y = (self.screen_height - self.maze_height_px) / 2

    def cell_to_pixel(self, cell: tuple[int, int]) -> tuple[float, float]:
        """Convert a ``(row, col)`` grid cell to on-screen pixel coordinates.
        """
        row, col = cell
        pixel_x = col * self.cell_width_px + self.offset_x \
            + constant.WALL_WIDTH * 1.3
        pixel_y = row * self.cell_height_px + self.offset_y \
            + constant.WALL_WIDTH * 1.3
        return (pixel_x, pixel_y)

    def pixel_to_cell(self, pixel: tuple[int, int]) -> tuple[int, int]:
        """Convert on-screen pixel coordinates to a ``(row, col)`` grid cell.
        """
        pixel_x, pixel_y = pixel
        col = (pixel_x - self.offset_x) // self.cell_width_px
        row = (pixel_y - self.offset_y) // self.cell_height_px
        return (int(row), int(col))
