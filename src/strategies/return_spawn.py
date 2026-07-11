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
        phantom_cell: tuple[int, int],
        player_cell: tuple[int, int],
        prev_phantom_cell: tuple[int, int] | None = None
    ) -> list[tuple[int, int]]:
        return self.get_path(phantom_cell, self.target_cell)
