from .strategy import Strategy


class ZoneStrategy(Strategy):
    def __init__(
            self,
            map_grid: list[list[int]],
            name: str = "Zone"
    ) -> None:
        super().__init__(map_grid=map_grid, name=name)

    # Will take a zone to move in then circle in it until every spot has been
    # used 1 time
    def mouvement(
        self,
        start: tuple[int, int],
        goal: tuple[int, int]
    ):
        return self.get_path(start, goal)
