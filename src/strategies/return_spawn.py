from .strategy import Strategy


class ReturnToSpawnStrategy(Strategy):
    def __init__(
        self,
        map_grid: list[list[int]],
        phantom_pos: tuple[int, int],
        name: str = "Spawn"
    ) -> None:
        super().__init__(map_grid=map_grid, name=name)
        self.target: tuple[int, int] = phantom_pos
        self.path: list[tuple[int, int]] = []

    def movement(
        self,
        phantom_pos,
        player_pos,
        prev_phantom_pos=None
    ) -> list[tuple[int, int]]:
        return self.get_path(phantom_pos, self.target)
