from .strategy import Strategy


class MimicStrategy(Strategy):
    def __init__(
            self,
            map_grid: list[list[int]],
            name: str = "Mimic"
    ) -> None:
        super().__init__(map_grid=map_grid, name=name)

    # Will mimic the player mouvements
    def movement(self):
        return super().movement()
