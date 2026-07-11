from .strategy import Strategy
import random


class ZoneStrategy(Strategy):
    def __init__(
            self,
            map_grid: list[list[int]],
            name: str = "Zone"
    ) -> None:
        super().__init__(map_grid=map_grid, name=name)
        self.zone: list[tuple[int, int]] = []
        self.possible_rows: list[int] = [
            0,
            len(self.map_grid) // 2,
            len(self.map_grid) - 1,
        ]
        self.possible_cols: list[int] = [
            0,
            len(self.map_grid[0]) // 2,
            len(self.map_grid[0]) - 1,
        ]
        self.make_zone()

    def movement(
        self,
        phantom_cell: tuple[int, int],
        player_cell: tuple[int, int],
        prev_phantom_cell: tuple[int, int] | None = None
    ) -> list[tuple[int, int]]:
        if len(self.zone) == 0:
            self.make_zone()
        goal_cell = random.choice(self.zone)
        self.zone.remove(goal_cell)
        return self.get_path(phantom_cell, goal_cell)

    def make_zone(
        self,
    ) -> None:
        rows = random.sample(self.possible_rows, 2)
        cols = random.sample(self.possible_cols, 2)
        start_row, end_row = min(rows), max(rows)
        start_col, end_col = min(cols), max(cols)
        self.zone = []
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if self.map_grid[row][col] == 15:
                    continue
                self.zone.append((row, col))
