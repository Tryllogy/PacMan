from .base_strategy import Strategy


class RetreatStrategy(Strategy):
    def __init__(
            self,
            name: str = "Retreat"
    ) -> None:
        super().__init__(name)

    # Will go away as far as possible from the player
    def mouvement(self):
        pass
