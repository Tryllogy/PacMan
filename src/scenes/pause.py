from .scene import Scene, GameState
import pygame


class PauseScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.current_scene = GameState.PAUSE.value
        self.base_scene = self.current_scene

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.current_scene = GameState.GAME.value
        return self.current_scene

    def back_ingame(
            self
    ) -> str:
        self.current_scene = GameState.GAME.value
        return self.current_scene

    def draw(
        self,
    ):
        super().draw()

    def update(
        self
    ) -> str:
        return self.current_scene
