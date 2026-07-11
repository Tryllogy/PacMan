import pygame
from .. import constant


class Pacgum:
    def __init__(
        self,
        pixel_x: int,
        pixel_y: int
    ):
        self.pixel_x: int = pixel_x
        self.pixel_y: int = pixel_y
        self.rect: pygame.Rect = pygame.Rect(
            self.pixel_x - constant.PACGUM_SIZE // 2,
            self.pixel_y - constant.PACGUM_SIZE // 2,
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
