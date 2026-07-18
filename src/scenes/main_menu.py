from .scene import Scene, GameState
from .. import constant
from ..graphics import Event, EventType, app, Surface
from ..graphics import events as ev


MENU_LINES = [
    ("PAC-MAN", (255, 255, 0), -160),
    ("1 - Play", constant.TEXT_COLOR_BASE, -40),
    ("2 - View highscore", constant.TEXT_COLOR_BASE, 0),
    ("3 - Instructions", constant.TEXT_COLOR_BASE, 40),
    ("ESC - Exit", constant.TEXT_COLOR_BASE, 80),
]


class MainScene(Scene):
    def __init__(
        self,
        screen: Surface
    ) -> None:
        super().__init__(screen)
        self.current_scene = GameState.MAIN.value
        self.base_scene = self.current_scene

    def handle_events(
        self,
        events: list[Event]
    ) -> str:
        for event in events:
            if event.type != EventType.KEYDOWN:
                continue
            if event.key == ev.K_ESCAPE:
                app.request_exit()
            elif event.key == ev.K_1:
                self.current_scene = GameState.GAME.value
            elif event.key == ev.K_2:
                self.current_scene = GameState.HIGHSCORE.value
            elif event.key == ev.K_3:
                self.current_scene = GameState.INSTRUCTIONS.value
        return self.current_scene

    def draw(
        self,
    ) -> None:
        super().draw()
        mx, my = self.middle_screen
        for text, color, dy in MENU_LINES:
            surface = self.font.render(text, True, color)
            self.screen.blit(surface, surface.get_rect(center=(mx, my + dy)))

    def update(
        self
    ) -> str:
        return self.current_scene
