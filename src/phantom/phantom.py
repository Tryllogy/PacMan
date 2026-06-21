from ..strategies import Strategy


class Phantom:
    def __init__(
            self,
            strategy: Strategy,
            color: str,
    ):
        self.strategy: Strategy = strategy
        self.color: str = color

    def change_strategy(
            self,
            strategy: Strategy
    ):
        if not isinstance(strategy, Strategy):
            raise TypeError(f"Not a valid strategy: {strategy}")
        self.strategy = strategy

    # Base on strategy it will move differently from other phantoms
    def move(self):
        pass
