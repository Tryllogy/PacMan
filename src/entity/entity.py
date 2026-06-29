from abc import ABC, abstractmethod
from enum import Enum
import pygame
from .. import constant


class Direction(Enum):
    UP: str = "up"
    DOWN: str = "down"
    LEFT: str = "left"
    RIGHT: str = "right"


class Entity(ABC):
    def __init__(
        self,
        x: int,
        y: int
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.spawn_x: int = x
        self.spawn_y: int = y
        self.sprites: list[pygame.Surface] = []

    @abstractmethod
    def update(
        self
    ) -> None:
        pass

    @abstractmethod
    def draw(
        self,
        screen: pygame.Surface
    ) -> None:
        pass

    def is_aligned(
            self,
    ) -> bool:
        return (
            (self.x - self.origin_x) % constant.WALL_HEIGHT == 0 and
            (self.y - self.origin_y) % constant.WALL_HEIGHT == 0
        )
