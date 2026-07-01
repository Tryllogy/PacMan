from abc import ABC, abstractmethod


class Strategy(ABC):
    def __init__(
            self,
            name: str
    ):
        self.name: str = name

    @abstractmethod
    def get_path(
        self,
        self_pos: tuple[int, int],
        player_pos: tuple[int, int]
            ) -> list[tuple[int, int]]:
        pass

    # Will go to his spawnpoint if killed by player (can be not abstract)
    # @abstractmethod
    def to_spawn(self):
        pass
