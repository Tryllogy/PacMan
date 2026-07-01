from .scene import Scene, GameState
import pygame


class WinScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.current_scene = GameState.WIN.value
        self.base_scene = self.current_scene
        self.font: pygame.font.Font = pygame.font.Font(None, 74)
        self.win_text = self.font.render("You Win!", True, (0, 255, 0))
        self.win_text_rect = self.win_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

    def handle_events(
        self,
        events
    ) -> str:
        return self.current_scene

    def draw(
        self,
        screen: pygame.Surface
    ):
        super().draw(screen)
        self.screen.blit(self.win_text, self.win_text_rect)

    def update(
        self
    ) -> str:
        return self.current_scene
