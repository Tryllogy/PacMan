import os
from .scene import Scene, GameState
from ..entity import load_highscores
from ..graphics import Event, EventType, Surface
from ..graphics import events as ev
from .. import constant


class HighscoreScene(Scene):
    def __init__(
        self,
        screen: Surface,
        filename: str,
    ) -> None:
        super().__init__(screen)
        self.current_scene = GameState.HIGHSCORE.value
        self.base_scene = self.current_scene
        self.filename: str = filename
        self.retrieve_highscores()

    def retrieve_highscores(
        self
    ) -> None:
        self.highscores: list[dict] = load_highscores(
            os.path.join(constant.SCORE_DIR, self.filename))

    def handle_events(self, events: list[Event]) -> str:
        for event in events:
            if event.type == EventType.KEYDOWN and event.key == ev.K_ESCAPE:
                self.current_scene = GameState.MAIN.value
        return self.current_scene

    def draw_highscores(
        self
    ) -> None:
        x, y = self.middle_screen
        title = self.font.render(
            "Highscores  (ESC - Back)", True, (255, 255, 0))
        self.screen.blit(title, title.get_rect(center=(x, y - 260)))
        if len(self.highscores) == 0:
            text = self.font.render(
                "No highscores yet.", True, constant.TEXT_COLOR_BASE)
            self.screen.blit(text, text.get_rect(center=(x, y - 200)))
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
        super().draw()
        self.draw_highscores()

    def update(
        self
    ) -> str:
        self.retrieve_highscores()
        return self.current_scene
