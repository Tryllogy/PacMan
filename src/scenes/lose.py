from .scene import Scene


class LoseScene(Scene):

    def handle_events(self, events):
        return super().handle_events(events)

    def draw(
        self,
    ):
        super().draw()
