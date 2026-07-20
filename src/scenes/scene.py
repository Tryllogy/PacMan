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
        """Set up the shared font, screen and scene-state attributes."""
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
        """Compute and store the screen's centre point."""
        width: int = screen.get_width() // 2
        height: int = screen.get_height() // 2
        self.middle_screen = (width, height)
        return self.middle_screen

    @abstractmethod
    def handle_events(
        self,
        events: list[pygame.event.Event]
    ) -> str:
        """Handle input events and return the next scene's state key."""
        pass

    @abstractmethod
    def update(self) -> str:
        """Advance the scene one frame and return the next scene's state key.
        """
        pass

    @abstractmethod
    def draw(
        self,
    ) -> None:
        """Render the scene onto its screen."""
        self.screen.fill((0, 0, 0))
