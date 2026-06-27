import pygame
from ... import constant


class SuperPacgum:
    def __init__(
        self,
        x: int,
        y: int
    ):
        self.x: int = x
        self.y = y

    def draw(
        self,
        screen: pygame.Surface,
    ):
        pygame.draw.circle(
            screen,
            constant.SUPERPACGUM_COLOR,
            (self.x, self.y),
            constant.SUPERPACGUM_SIZE
        )
