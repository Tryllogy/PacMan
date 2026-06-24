from .scene import Scene


class InGameScene(Scene):
    def draw(
        self,
        mouse_pos: tuple[int, int]
    ):
        return super().draw(mouse_pos)
