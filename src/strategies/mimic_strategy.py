from .strategy import Strategy


class MimicStrategy(Strategy):
    def __init__(
            self,
            name: str = "Mimic"
    ) -> None:
        super().__init__(name)

    # Will mimic the player mouvements
    def movement(self):
        return super().mouvement()
