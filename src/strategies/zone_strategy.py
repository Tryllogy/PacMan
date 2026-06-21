from .base_strategy import Strategy


class ZoneStrategy(Strategy):
    def __init__(
            self,
            name: str = "Zone"
    ) -> None:
        super().__init__(name)

    # Will take a zone to move in then circle in it until every spot has been
    # used 1 time
    def mouvement(self):
        return super().mouvement()
