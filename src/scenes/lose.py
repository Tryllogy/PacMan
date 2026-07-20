import pygame
from .end_scene import EndScene
from .scene import GameState
from ..parsing import Data
from ..entity import Score


class LoseScene(EndScene):
    def __init__(
        self,
        screen: pygame.Surface,
        config: Data,
        score: Score
    ) -> None:
        """Build the lose screen with its red title."""
        super().__init__(
            screen, config, score,
            GameState.LOSE, "You Lose!", (255, 0, 0))
