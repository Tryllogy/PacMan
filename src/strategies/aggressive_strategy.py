from .base_strategy import Strategy


class AggressiveStrategy(Strategy):
    def __init__(
            self,
            name: str = "Aggressive"
    ) -> None:
        super().__init__(name)

    # Will follow the player everytime
    def mouvement(self):
        pass
