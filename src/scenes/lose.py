from .scene import Scene


class LoseScene(Scene):
    def draw(
        self,
        mouse_pos: tuple[int, int]
    ):
        return super().draw(mouse_pos)
