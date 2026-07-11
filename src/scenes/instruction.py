import pygame
from .scene import Scene, GameState
from .button import Button
from .. import constant


class InstructionsScene(Scene):
    def __init__(
        self,
        screen: pygame.Surface
    ) -> None:
        super().__init__(screen)
        self.current_scene = GameState.INSTRUCTIONS.value
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
        self.instructions_text: str = (
            "Instructions:\n"
            "Use the arrow keys or WASD to move Pac-Man.\n"
            "Eat all the dots to win!\n"
            "Avoid the ghosts or you'll lose a life.\n"
            "Press 'I' to toggle invincibility.\n"
            "Press 'P' to start a new level.\n"
            "Press 'ESC' to pause the game."
        )
        self.instructions_lines: list[str] = self.instructions_text.split("\n")
        self.instructions_surfaces: list[pygame.Surface] = [
            self.font.render(line, True, constant.TEXT_COLOR_BASE)
            for line in self.instructions_lines
        ]

    def back_main(
            self
    ) -> str:
        self.current_scene = GameState.MAIN.value
        return self.current_scene

    def handle_events(self, events: list[pygame.event.Event]) -> str:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.current_scene = GameState.MAIN.value
            self.back_button.handle_event(event)
        return self.current_scene

    def draw(
        self,
    ) -> None:
        self.back_button.draw(self.screen)
        self.draw_instructions()

    def update(
        self
    ) -> str:
        return self.current_scene

    def draw_instructions(
        self
    ) -> None:
        x, y = self.middle_screen
        for i, surface in enumerate(self.instructions_surfaces):
            text_rect = surface.get_rect(center=(x, y - 100 + i * 40))
            self.screen.blit(surface, text_rect)
