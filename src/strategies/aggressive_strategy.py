from .strategy import Strategy


class AggressiveStrategy(Strategy):
    def __init__(
        self,
        map_grid: list[list[int]],
        name: str = "Aggressive"
    ) -> None:
        super().__init__(map_grid=map_grid, name=name)

    def movement(
        self,
        phantom_cell: tuple[int, int],
        player_cell: tuple[int, int],
        prev_phantom_cell: tuple[int, int] | None = None
    ) -> list[tuple[int, int]]:
        return self.get_path(phantom_cell, player_cell)
