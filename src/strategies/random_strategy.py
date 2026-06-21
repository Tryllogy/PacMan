from .base_strategy import Strategy


class RandomStrategy(Strategy):
    def __init__(
            self,
            name: str = "Random"
    ) -> None:
        super().__init__(name)

    # Will take a point in maze a move to
    def mouvement(self):
        return super().mouvement()
