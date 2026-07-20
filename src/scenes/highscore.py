import os
import pygame
from .scene import Scene, GameState
from .button import Button
from ..entity import load_highscores
from .. import constant


class HighscoreScene(Scene):
    def __init__(
        self,
        screen: pygame.Surface,
        filename: str,
    ) -> None:
        """Build the highscore screen and load the scores from ``filename``."""
        super().__init__(screen)
        self.current_scene = GameState.HIGHSCORE.value
        self.base_scene = self.current_scene
        x, y = self.middle_screen
        self.back_button: Button = Button(
            x - 150,
            y + 300,
            constant.BUTTON_WIDTH,
            constant.BUTTON_HEIGHT,
            "Back",
            self.back_main,
            self.font
        )
        self.filename: str = filename
        self.retrieve_highscores()

    def retrieve_highscores(
        self
    ) -> None:
        """Load highscores from the file, handling errors gracefully."""
        self.highscores: list[dict] = load_highscores(
            os.path.join(constant.SCORE_DIR, self.filename))

    def back_main(
        self
    ) -> str:
        """Return to the main scene."""
        self.current_scene = GameState.MAIN.value
        return self.current_scene

    def handle_events(self, events: list[pygame.event.Event]) -> str:
        """Handle events for the highscore scene, including back button and
        ESC key."""
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.current_scene = GameState.MAIN.value
            self.back_button.handle_event(event)
        return self.current_scene

    def draw_highscores(
        self
    ) -> None:
        """Render the top-10 scores, or a placeholder when there are none."""
        x, y = self.middle_screen
        if len(self.highscores) == 0:
            text = self.font.render(
                "No highscores yet.",
                True,
                constant.TEXT_COLOR_BASE
            )
            self.screen.blit(text, (x - 100, y - 200))
        else:
            for i, score in enumerate(self.highscores):
                if i >= 10:
                    break
                text = self.font.render(
                    f"{i + 1}. {score['name']} - {score['score']}",
                    True,
                    constant.TEXT_COLOR_BASE
                )
                self.screen.blit(text, (x - 100, y - 200 + i * 40))

    def draw(
        self,
    ) -> None:
        """Draw the Back button and the highscore list."""
        self.back_button.draw(self.screen)
        self.draw_highscores()

    def update(
        self
    ) -> str:
        """Reload the highscores each frame and return the scene key.
        """
        self.retrieve_highscores()
        return self.current_scene
