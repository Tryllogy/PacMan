from .scene import Scene, GameState


class WinScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.current_scene = GameState.WIN.value
        self.base_scene = self.current_scene

    def handle_events(self, events):
        return super().handle_events(events)

    def draw(
        self,
    ):
        super().draw()
