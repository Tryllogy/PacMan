import pygame
import json
from .scene import Scene, GameState
from .button import Button
from .. import constant


class HighscoreScene(Scene):
    def __init__(
        self,
        screen: pygame.Surface,
        filename: str,
    ) -> None:
        super().__init__(screen)
        self.font: pygame.font.Font = pygame.font.Font(None, 36)
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
        try:
            with open(constant.SCORE_DIR + self.filename, "r") as f:
                self.highscores: list[dict] = json.loads(f.read())
            self.highscores.sort(key=lambda x: x["score"], reverse=True)
        except FileNotFoundError:
            self.highscores: list[dict] = []

    def back_main(
        self
    ) -> str:
        self.current_scene = GameState.MAIN.value
        return self.current_scene

    def handle_events(self, events):
        for event in events:
            self.back_button.handle_event(event)
        return self.current_scene

    def draw_highscores(
        self
    ) -> None:
        x, y = self.middle_screen
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
        self.back_button.draw(self.screen)
        self.draw_highscores()

    def update(
        self
    ) -> str:
        self.retrieve_highscores()
        return self.current_scene
