import json
import os
import pygame
from .scene import Scene, GameState
from ..parsing import Data
from ..entity import Score
from .. import constant


class EndScene(Scene):
    """Base scene shown when the game ends (win or lose).

    Displays a title and the final score, lets the player type their
    name, and persists it to the highscore file. Subclasses only provide
    the game state, the title text and its color.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        config: Data,
        score: Score,
        state: GameState,
        title: str,
        title_color: tuple[int, int, int],
    ) -> None:
        super().__init__(screen)
        self.current_scene = state.value
        self.base_scene = self.current_scene
        self.font: pygame.font.Font = pygame.font.Font(None, 74)
        self.title_text = self.font.render(title, True, title_color)
        self.title_text_rect = self.title_text.get_rect(
            center=self.middle_screen)
        self.name_user: str = ""
        self.score: Score = score
        self.config: Data = config

    def write_name_to_file(
        self
    ) -> None:
        file_path = os.path.join(constant.SCORE_DIR,
                                 self.config.highscore_filename)
        if not os.path.exists(constant.SCORE_DIR):
            os.makedirs(constant.SCORE_DIR)
        scores: list = []
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    scores = json.load(f)
                if not isinstance(scores, list):
                    scores = []
            except (json.JSONDecodeError, ValueError):
                scores = []
        scores.append({"name": self.name_user, "score": self.score.score})
        with open(file_path, "w") as f:
            json.dump(scores, f, indent=4)

    def draw_name_user_text(
        self
    ) -> None:
        self.name_user_text = self.font.render(
            f"Enter your name: {self.name_user}", True, (255, 255, 255))
        self.name_user_text_rect = self.name_user_text.get_rect(
            center=(self.middle_screen[0], self.middle_screen[1] + 100))
        self.screen.blit(self.name_user_text, self.name_user_text_rect)

    def handle_events(
        self,
        events
    ) -> str:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.name_user = self.name_user[:-1]
                if event.key == pygame.K_RETURN:
                    self.write_name_to_file()
                    return GameState.MAIN.value
                else:
                    self.name_user += event.unicode
        return self.current_scene

    def draw(
        self,
    ) -> None:
        super().draw()
        self.screen.blit(self.title_text, self.title_text_rect)
        score_txt = self.font.render(
            f"Your score: {self.score.score}", True, (255, 255, 255))
        score_txt_rect = score_txt.get_rect(
            center=(self.middle_screen[0], self.middle_screen[1] + 50))
        self.screen.blit(score_txt, score_txt_rect)
        self.draw_name_user_text()

    def update(
        self
    ) -> str:
        return self.current_scene
