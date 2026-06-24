from .scene import Scene


class HighscoreScene(Scene):

    def handle_events(self, events):
        return super().handle_events(events)

    def draw(
        self,
        mouse_pos: tuple[int, int]
    ):
        return super().draw(mouse_pos)
