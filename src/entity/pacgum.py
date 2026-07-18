from ..graphics import Surface, Rect
from .. import constant


class Pacgum:
    def __init__(
        self,
        pixel_x: int,
        pixel_y: int
    ):
        self.pixel_x: int = pixel_x
        self.pixel_y: int = pixel_y
        self.rect: Rect = Rect(
            self.pixel_x - constant.PACGUM_SIZE // 2,
            self.pixel_y - constant.PACGUM_SIZE // 2,
            constant.PACGUM_SIZE,
            constant.PACGUM_SIZE
        )

    def draw(
        self,
        screen: Surface,
    ) -> None:
        screen.draw_circle(
            constant.PACGUM_COLOR,
            self.rect.center,
            self.rect.width // 2
        )
