from abc import ABC, abstractmethod
from enum import Enum
import pygame
from .. import constant


class Direction(Enum):
    UP: str = "up"
    DOWN: str = "down"
    LEFT: str = "left"
    RIGHT: str = "right"
    NONE: str = "none"

    # Maze positions are (line, column), so index 0 moves along y
    @classmethod
    def from_maze_delta(
        cls,
        start: tuple[int, int],
        end: tuple[int, int]
    ) -> "Direction":
        d_line = end[0] - start[0]
        d_col = end[1] - start[1]
        if d_col > 0:
            return cls.RIGHT
        if d_col < 0:
            return cls.LEFT
        if d_line > 0:
            return cls.DOWN
        if d_line < 0:
            return cls.UP
        return cls.NONE


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
