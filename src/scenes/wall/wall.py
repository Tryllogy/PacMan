import pygame
from ... import constant


class Wall:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:
        pygame.draw.rect(
            screen,
            constant.WALL_COLOR,
            pygame.Rect(
                self.x,
                self.y,
                self.width,
                self.height,
             ),
        )
