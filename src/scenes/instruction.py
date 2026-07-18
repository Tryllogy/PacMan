from .scene import Scene, GameState
from ..graphics import Event, EventType, Surface
from ..graphics import events as ev
from .. import constant


class InstructionsScene(Scene):
    def __init__(
        self,
        screen: Surface
    ) -> None:
        super().__init__(screen)
        self.current_scene = GameState.INSTRUCTIONS.value
        self.base_scene = self.current_scene
        self.instructions_text: str = (
            "Instructions:\n"
            "Use the arrow keys or WASD to move Pac-Man.\n"
            "Eat all the dots to win!\n"
            "Avoid the ghosts or you'll lose a life.\n"
            "Press 'I' to toggle invincibility.\n"
            "Press 'P' to start a new level.\n"
            "Press 'ESC' to pause the game.\n"
            "Press 'ESC' here to go back."
        )
        self.instructions_lines: list[str] = self.instructions_text.split("\n")

    def handle_events(self, events: list[Event]) -> str:
        for event in events:
            if event.type == EventType.KEYDOWN and event.key == ev.K_ESCAPE:
                self.current_scene = GameState.MAIN.value
        return self.current_scene

    def draw(
        self,
    ) -> None:
        super().draw()
        self.draw_instructions()

    def update(
        self
    ) -> str:
        return self.current_scene

    def draw_instructions(
        self
    ) -> None:
        x, y = self.middle_screen
        for i, line in enumerate(self.instructions_lines):
            surface = self.font.render(line, True, constant.TEXT_COLOR_BASE)
            self.screen.blit(surface, surface.get_rect(
                center=(x, y - 140 + i * 40)))
