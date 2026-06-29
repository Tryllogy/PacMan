import pygame
from ... import constant


class Pacgum:
    def __init__(
        self,
        x: int,
        y: int
    ):
        self.x: int = x
        self.y: int = y
        self.rect: pygame.Rect = pygame.Rect(
            self.x - constant.PACGUM_SIZE // 2,
            self.y - constant.PACGUM_SIZE // 2,
            constant.PACGUM_SIZE,
            constant.PACGUM_SIZE
        )

    def draw(
        self,
        screen: pygame.Surface,
    ):
        pygame.draw.circle(
            screen,
            constant.PACGUM_COLOR,
            self.rect.center,
            self.rect.width // 2
        )
