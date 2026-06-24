from .scene import Scene, GameState
import pygame


class InGameScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.current_scene = GameState.GAME.value
        mx, my = self.middle_screen

    def handle_events(
        self,
        events
    ) -> str:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                print("PAUSE")
        return self.current_scene

    def draw(
        self,
    ) -> None:
        super().draw()
