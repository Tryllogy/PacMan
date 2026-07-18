from .scene import Scene, GameState
from ..graphics import Event, EventType, app, Surface
from ..graphics import events as ev


PAUSE_LINES = [
    ("Game Paused", (255, 255, 255), -80),
    ("ESC - Resume", (255, 255, 255), 0),
    ("M - Main Menu", (255, 255, 255), 40),
    ("Q - Exit", (255, 255, 255), 80),
]


class PauseScene(Scene):
    def __init__(self, screen: Surface) -> None:
        super().__init__(screen)
        self.current_scene = GameState.PAUSE.value
        self.base_scene = self.current_scene

    def handle_events(self, events: list[Event]) -> str:
        for event in events:
            if event.type != EventType.KEYDOWN:
                continue
            if event.key == ev.K_ESCAPE:
                self.current_scene = GameState.GAME.value
            elif event.key == ev.K_m:
                self.current_scene = GameState.MAIN.value
            elif event.key == ev.K_q:
                app.request_exit()
        return self.current_scene

    def draw(
        self,
    ) -> None:
        super().draw()
        mx, my = self.middle_screen
        for text, color, dy in PAUSE_LINES:
            surface = self.font.render(text, True, color)
            self.screen.blit(surface, surface.get_rect(center=(mx, my + dy)))

    def update(
        self
    ) -> str:
        return self.current_scene
