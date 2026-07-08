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

    def get_goal(self):
        available_points: list[tuple[int, int]] = []
        for y, row in enumerate(self.map_grid):
            for x, cell in enumerate(row):
                if cell == 15:
                    continue
                if (x, y) == self.phantom_pos:
                    continue
                available_points.append((x, y))
        goal = random.choice(available_points)
        return goal

    # Will take a point in maze a move to
    def movement(
        self,
        start: tuple[int, int]
    ) -> list[tuple[int, int]]:
        self.phantom_pos = start
        # print("target", self.target, "phantome pos", self.phantom_pos)
        if self.target != self.phantom_pos:
            return self.path
        self.target = self.get_goal()
        Strategy.set_rand_pos(self.target)
        # print("self.path", self.path)
        # print("self.target", self.target)
        return self.get_path(start, 'rand')
