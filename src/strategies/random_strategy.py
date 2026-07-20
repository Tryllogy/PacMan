from .strategy import Strategy
import random


class RandomStrategy(Strategy):
    def __init__(
            self,
            map_grid: list[list[int]],
            phantom_cell: tuple[int, int],
            name: str = "Random"
    ) -> None:
        """Create the random-roaming strategy starting at ``phantom_cell``."""
        super().__init__(map_grid=map_grid, name=name)
        self.target_cell: tuple[int, int] = phantom_cell
        self.phantom_cell: tuple[int, int] = phantom_cell
        self.path: list[tuple[int, int]] = []

    def get_goal(self) -> tuple[int, int]:
        """Pick a random open cell (not a full wall, not the current one)."""
        available_cells: list[tuple[int, int]] = []
        for row, line in enumerate(self.map_grid):
            for col, value in enumerate(line):
                if value == 15:
                    continue
                if (row, col) == self.phantom_cell:
                    continue
                available_cells.append((row, col))
        goal_cell = random.choice(available_cells)
        return goal_cell

    def movement(
        self,
        phantom_cell: tuple[int, int],
        player_cell: tuple[int, int],
        prev_phantom_cell: tuple[int, int] | None = None
    ) -> list[tuple[int, int]]:
        """Path toward the current random target, picking a new one on arrival.
        """
        self.phantom_cell = phantom_cell
        if self.target_cell == self.phantom_cell:
            self.target_cell = self.get_goal()
        return self.get_path(self.phantom_cell, self.target_cell)
