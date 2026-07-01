from .strategy import Strategy
import random


class RandomStrategy(Strategy):
    def __init__(
            self,
            map_grid: list[list[int]],
            phantom_pos: tuple[int, int],
            name: str = "Random"
    ) -> None:
        super().__init__(map_grid=map_grid, name=name)
        self.phantom_pos: tuple[int, int] = phantom_pos
        self.target: tuple[int, int] = phantom_pos
        self.path: list[tuple[int, int]] = []

    # Will take a point in maze a move to
    def movement(
        self,
        start: tuple[int, int],
        goal: tuple[int, int]
    ) -> list[tuple[int, int]]:
        if self.target != self.phantom_pos:
            self.phantom_pos = start
            return self.path
        available_points: list[tuple[int, int]] = []
        for y, row in enumerate(self.map_grid):
            for x, cell in enumerate(row):
                if cell == 15:
                    continue
                available_points.append((x, y))
        goal = random.choice(available_points)
        self.target = goal
        self.path = self.get_path(start, goal)
        return self.path
