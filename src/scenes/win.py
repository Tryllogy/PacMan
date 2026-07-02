import pygame
import os
import json
from .scene import Scene, GameState
from .. import constant
from ..parsing import Data
from ..entity import Score


class WinScene(Scene):
    def __init__(
        self,
        screen: pygame.Surface,
        config: Data,
        score: Score
    ) -> None:
        super().__init__(screen)
        self.current_scene = GameState.WIN.value
        self.base_scene = self.current_scene
        self.font: pygame.font.Font = pygame.font.Font(None, 74)
        self.win_text = self.font.render("You Win!", True, (0, 255, 0))
        self.win_text_rect = self.win_text.get_rect(
            center=self.middle_screen)
        self.name_user: str = ""
        self.score: Score = score
        self.config: Data = config
        self.score_txt = self.font.render(
            f"Your score: {self.score.score}", True, (255, 255, 255))
        self.score_txt_rect = self.score_txt.get_rect(
            center=(self.middle_screen[0], self.middle_screen[1] + 50))

    def write_name_to_file(
        self
    ) -> None:
        file_path = os.path.join(constant.SCORE_DIR,
                                 self.config.highscore_filename)
        if not os.path.exists(constant.SCORE_DIR):
            os.makedirs(constant.SCORE_DIR)
        with open(file_path, "a") as f:
            json.dump({"name": self.name_user, "score": self.score.score}, f)

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
    ):
        super().draw()
        self.screen.blit(self.win_text, self.win_text_rect)
        self.screen.blit(self.score_txt, self.score_txt_rect)
        self.draw_name_user_text()

    def update(
        self
    ) -> str:
        return self.current_scene
