from .strategy import Strategy


class ReturnToSpawnStrategy(Strategy):
    def __init__(
        self,
        map_grid: list[list[int]],
        phantom_cell: tuple[int, int],
        name: str = "Spawn"
    ) -> None:
        super().__init__(map_grid=map_grid, name=name)
        self.target_cell: tuple[int, int] = phantom_cell
        self.path: list[tuple[int, int]] = []

    def movement(
        self,
        phantom_cell,
        player_cell,
        prev_phantom_cell=None
    ) -> list[tuple[int, int]]:
        return self.get_path(phantom_cell, self.target_cell)
