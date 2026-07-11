import os
import pygame
from .scene import Scene, GameState
from ..parsing import Data
from ..entity import (
    Score, save_highscore, sanitize_name_char,
)
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
        subtitle: str = "",
    ) -> None:
        super().__init__(screen)
        self.current_scene = state.value
        self.base_scene = self.current_scene
        self.title_text = self.font.render(title, True, title_color)
        self.title_text_rect = self.title_text.get_rect(
            center=self.middle_screen)
        self.subtitle_text: pygame.Surface | None = None
        if subtitle:
            self.subtitle_text = self.font.render(
                subtitle, True, (255, 255, 255))
            self.subtitle_text_rect = self.subtitle_text.get_rect(
                center=(self.middle_screen[0], self.middle_screen[1] - 60))
        self.name_user: str = ""
        self.score: Score = score
        self.config: Data = config

    def write_name_to_file(
        self
    ) -> bool:
        if len(self.name_user.strip()) == 0:
            return False
        file_path = os.path.join(constant.SCORE_DIR,
                                 self.config.highscore_filename)
        save_highscore(file_path, self.name_user, self.score.score)
        self.name_user = ""
        return True

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
                if event.key == pygame.K_ESCAPE:
                    import sys
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_BACKSPACE:
                    if len(self.name_user) > 0:
                        self.name_user = self.name_user[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.write_name_to_file():
                        return GameState.MAIN.value
                else:
                    char = sanitize_name_char(event.unicode)
                    if char and len(self.name_user) < constant.MAX_NAME_LENGTH:
                        self.name_user += char
        return self.current_scene

    def draw(
        self,
    ) -> None:
        super().draw()
        self.screen.blit(self.title_text, self.title_text_rect)
        if self.subtitle_text is not None:
            self.screen.blit(self.subtitle_text, self.subtitle_text_rect)
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
