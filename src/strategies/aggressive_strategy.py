from .strategy import Strategy


class AggressiveStrategy(Strategy):
    def __init__(
        self,
        map_grid: list[list[int]],
        name: str = "Aggressive"
    ) -> None:
        super().__init__(map_grid=map_grid, name=name)

    # Will follow the player everytime
    def movement(
        self,
        start: tuple[int, int],
        goal: tuple[int, int]
    ) -> list[tuple[int, int]]:
        # print("==============", start, goal)
        return self.get_path(start, goal)
