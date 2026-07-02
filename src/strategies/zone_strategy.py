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
        self.possible_x: list[int] = [
            0,
            len(self.map_grid) // 2,
            len(self.map_grid) - 1,
        ]
        self.possible_y: list[int] = [
            0,
            len(self.map_grid[0]) // 2,
            len(self.map_grid[0]) - 1,
        ]
        self.make_zone()

    # Will take a zone to move in then circle in it until every spot has been
    # used 1 time
    def movement(
        self,
        start: tuple[int, int],
        goal: tuple[int, int]
    ):
        if len(self.zone) == 0:
            self.make_zone()
        goal = random.choice(self.zone)
        self.zone.remove(goal)
        return self.get_path(start, goal)

    def make_zone(
        self,
    ) -> bool:
        start_x, end_x = random.sample(self.possible_x, 2)
        start_y, end_y = random.sample(self.possible_y, 2)
        self.zone = []
        for i in range(start_x, end_x):
            for j in range(start_y, end_y):
                if self.map_grid[i][j] == 15:
                    continue
                self.zone.append((i, j))
