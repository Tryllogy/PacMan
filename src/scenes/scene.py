from abc import ABC, abstractmethod
from enum import Enum
import pygame


class GameState(Enum):
    MAIN: str = "main_menu"
    GAME: str = "game"
    PAUSE: str = "pause"
    WIN: str = "win"
    LOSE: str = "lose"
    HIGHSCORE: str = "highscore"
    INSTRUCTIONS: str = "instructions"


class Scene(ABC):
    def __init__(
            self,
            screen: pygame.Surface
    ):
        self.font: pygame.font.Font = pygame.font.Font(None, 40)
        self.screen: pygame.Surface = screen
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
        events
    ) -> GameState:
        pass

    def update(self) -> None:
        pass

    @abstractmethod
    def draw(
        self,
    ) -> None:
        self.screen.fill((0, 0, 0))

    def hover_text(
            self,
            txt_dimension: tuple[int, int],
            mouse_pos: tuple[int, int],
            pos_text: tuple[int, int]
    ) -> bool:
        x, y = pos_text
        tx, ty = txt_dimension
        mx, my = mouse_pos
        return x <= mx <= x + tx and y <= my <= y + ty
