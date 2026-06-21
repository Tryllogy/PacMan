from abc import ABC, abstractmethod


class Strategy(ABC):
    def __init__(
            self,
            name: str
    ):
        self.name: str = name

    @abstractmethod
    def mouvement(self):
        pass

    # Will go to his spawnpoint if killed by player (can be not abstract)
    # @abstractmethod
    def to_spawn(self):
        pass
