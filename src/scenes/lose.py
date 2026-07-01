from .scene import Scene, GameState
import pygame


class LoseScene(Scene):
    def __init__(
        self,
        screen
    ) -> None:
        super().__init__(screen)
        self.current_scene = GameState.LOSE.value
        self.base_scene = self.current_scene
        self.font: pygame.font.Font = pygame.font.Font(None, 74)
        self.lose_text = self.font.render("You Lose!", True, (255, 0, 0))
        self.lose_text_rect = self.lose_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

    def handle_events(
        self,
        events
    ) -> str:
        return self.current_scene

    def draw(
        self,
    ):
        super().draw()
        self.screen.blit(self.lose_text, self.lose_text_rect)

    def update(
        self
    ) -> str:
        return self.current_scene
