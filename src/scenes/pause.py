from .scene import Scene


class PauseScene(Scene):
    def draw(
        self,
        mouse_pos: tuple[int, int]
    ):
        return super().draw(mouse_pos)
