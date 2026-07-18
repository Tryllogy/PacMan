from ..graphics import Surface, Rect
from .. import constant


class Wall:
    def __init__(
        self,
        pixel_x: int,
        pixel_y: int,
        width: int,
        height: int,
    ) -> None:
        self.pixel_x: int = pixel_x
        self.pixel_y: int = pixel_y
        self.width: int = width
        self.height: int = height
        self.rect: Rect = Rect(
            self.pixel_x,
            self.pixel_y,
            self.width,
            self.height
        )

    def draw(
        self,
        screen: Surface,
    ) -> None:
        screen.draw_rect(
            constant.WALL_COLOR,
            self.rect,
        )
