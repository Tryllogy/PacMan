import pygame
from .. import constant


class SuperPacgum:
    def __init__(
        self,
        pixel_x: int,
        pixel_y: int
    ):
        self.pixel_x: int = pixel_x
        self.pixel_y: int = pixel_y
        self.rect: pygame.Rect = pygame.Rect(
            self.pixel_x - constant.SUPERPACGUM_SIZE // 2,
            self.pixel_y - constant.SUPERPACGUM_SIZE // 2,
            constant.SUPERPACGUM_SIZE,
            constant.SUPERPACGUM_SIZE
        )

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:
        pygame.draw.circle(
            screen,
            constant.SUPERPACGUM_COLOR,
            self.rect.center,
            self.rect.width // 2
        )
