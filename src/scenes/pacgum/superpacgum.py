import pygame
from ... import constant


class SuperPacgum:
    def __init__(
        self,
        x: int,
        y: int
    ):
        self.x: int = x
        self.y: int = y
        self.rect: pygame.Rect = pygame.Rect(
            self.x - constant.SUPERPACGUM_SIZE // 2,
            self.y - constant.SUPERPACGUM_SIZE // 2,
            constant.SUPERPACGUM_SIZE,
            constant.SUPERPACGUM_SIZE
        )

    def draw(
        self,
        screen: pygame.Surface,
    ):
        pygame.draw.circle(
            screen,
            constant.SUPERPACGUM_COLOR,
            self.rect.center,
            self.rect.width // 2
        )
