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
        self.rect: pygame.Rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:
        pygame.draw.rect(
            screen,
            constant.WALL_COLOR,
            self.rect,
        )
