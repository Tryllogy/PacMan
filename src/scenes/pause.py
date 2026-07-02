from .scene import Scene, GameState
import pygame
from .button import Button


class PauseScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.current_scene = GameState.PAUSE.value
        self.base_scene = self.current_scene
        self.pause_text = self.font.render(
            "Game Paused. Press 'ESC' to resume.",
            True,
            (255, 255, 255)
        )
        self.pause_text_rect = self.pause_text.get_rect(
            center=self.middle_screen
        )
        self.main_menu_button: Button = Button(
            self.middle_screen[0] - 75,
            self.middle_screen[1] + 50,
            150,
            50,
            "Main Menu",
            self.back_to_menu,
            self.font
        )
        self.exit_button: Button = Button(
            self.middle_screen[0] - 75,
            self.middle_screen[1] + 120,
            150,
            50,
            "Exit",
            self.exit_program,
            self.font
        )

    def handle_events(self, events):
        for event in events:
            self.main_menu_button.handle_event(event)
            self.exit_button.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.current_scene = GameState.GAME.value
        return self.current_scene

    def back_to_menu(
            self
    ) -> str:
        self.current_scene = GameState.MAIN.value
        return self.current_scene

    def exit_program(
            self
    ) -> None:
        import pygame
        import sys
        pygame.quit()
        sys.exit(0)

    def draw(
        self,
    ):
        super().draw()
        self.screen.blit(self.pause_text, self.pause_text_rect)
        self.main_menu_button.draw(self.screen)
        self.exit_button.draw(self.screen)

    def update(
        self
    ) -> str:
        return self.current_scene
