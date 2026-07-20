from .strategy import Strategy


class AggressiveStrategy(Strategy):
    def __init__(
        self,
        map_grid: list[list[int]],
        name: str = "Aggressive"
    ) -> None:
        """Create the aggressive (direct-chase) strategy for a maze."""
        super().__init__(map_grid=map_grid, name=name)

    def movement(
        self,
        phantom_cell: tuple[int, int],
        player_cell: tuple[int, int],
        prev_phantom_cell: tuple[int, int] | None = None
    ) -> list[tuple[int, int]]:
        """Return the A* path chasing the player straight to their cell."""
        return self.get_path(phantom_cell, player_cell)
