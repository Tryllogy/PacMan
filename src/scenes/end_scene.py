import os
from .scene import Scene, GameState
from ..parsing import Data
from ..entity import (
    Score, save_highscore, sanitize_name_char,
)
from ..graphics import Event, EventType, app, Surface
from ..graphics import events as ev
from .. import constant


class EndScene(Scene):
    """Base scene shown when the game ends (win or lose).

    Displays a title and the final score, lets the player type their
    name, and persists it to the highscore file. Subclasses only provide
    the game state, the title text and its color.
    """

    def __init__(
        self,
        screen: Surface,
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
        self.title: str = title
        self.title_color: tuple[int, int, int] = title_color
        self.subtitle: str = subtitle
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
        text = self.font.render(
            f"Enter your name: {self.name_user}", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(
            center=(self.middle_screen[0], self.middle_screen[1] + 100)))

    def handle_events(
        self,
        events: list[Event]
    ) -> str:
        for event in events:
            if event.type == EventType.KEYDOWN:
                if event.key == ev.K_ESCAPE:
                    app.request_exit()
                if event.key == ev.K_BACKSPACE:
                    if len(self.name_user) > 0:
                        self.name_user = self.name_user[:-1]
                        self.dirty = True
                elif event.key in (ev.K_RETURN, ev.K_KP_ENTER):
                    if self.write_name_to_file():
                        return GameState.MAIN.value
                else:
                    char = sanitize_name_char(event.char)
                    if char and len(self.name_user) < constant.MAX_NAME_LENGTH:
                        self.name_user += char
                        self.dirty = True
        return self.current_scene

    def draw(
        self,
    ) -> None:
        super().draw()
        mx, my = self.middle_screen
        title = self.font.render(self.title, True, self.title_color)
        self.screen.blit(title, title.get_rect(center=(mx, my)))
        if self.subtitle:
            sub = self.font.render(self.subtitle, True, (255, 255, 255))
            self.screen.blit(sub, sub.get_rect(center=(mx, my - 60)))
        score_txt = self.font.render(
            f"Your score: {self.score.score}", True, (255, 255, 255))
        self.screen.blit(score_txt, score_txt.get_rect(center=(mx, my + 50)))
        self.draw_name_user_text()

    def update(
        self
    ) -> str:
        return self.current_scene
