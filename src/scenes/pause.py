from .scene import Scene


class PauseScene(Scene):

    def handle_events(self, events):
        return super().handle_events(events)

    def draw(
        self,
    ):
        super().draw()
