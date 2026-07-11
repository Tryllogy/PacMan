from abc import ABC, abstractmethod
from enum import Enum
import pygame


class GameState(Enum):
    MAIN = "main_menu"
    GAME = "game"
    PAUSE = "pause"
    WIN = "win"
    LOSE = "lose"
    HIGHSCORE = "highscore"
    INSTRUCTIONS = "instructions"


class Scene(ABC):
    def __init__(
            self,
            screen: pygame.Surface
    ) -> None:
        self.font: pygame.font.Font = pygame.font.Font(None, 40)
        self.screen: pygame.Surface = screen
        self.current_scene: str = ""
        self.base_scene: str = ""
        self.middle_screen: tuple[int, int] = (0, 0)
        self.get_middle_screen(screen)

    def get_middle_screen(
            self,
            screen: pygame.Surface
    ) -> tuple[int, int]:
        width: int = screen.get_width() // 2
        height: int = screen.get_height() // 2
        self.middle_screen = (width, height)
        return self.middle_screen

    @abstractmethod
    def handle_events(
        self,
        events: list[pygame.event.Event]
    ) -> str:
        pass

    @abstractmethod
    def update(self) -> str:
        pass

    @abstractmethod
    def draw(
        self,
    ) -> None:
        self.screen.fill((0, 0, 0))
