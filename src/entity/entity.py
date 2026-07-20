from abc import ABC, abstractmethod
from enum import Enum
import pygame
from .. import constant


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    NONE = "none"

    @classmethod
    def from_cell_delta(
        cls,
        start_cell: tuple[int, int],
        end_cell: tuple[int, int]
    ) -> "Direction":
        """Return the direction to step from ``start_cell`` to ``end_cell``.

        Horizontal moves take priority over vertical ones; identical cells
        yield :attr:`Direction.NONE`.
        """
        d_row = end_cell[0] - start_cell[0]
        d_col = end_cell[1] - start_cell[1]
        if d_col > 0:
            return cls.RIGHT
        if d_col < 0:
            return cls.LEFT
        if d_row > 0:
            return cls.DOWN
        if d_row < 0:
            return cls.UP
        return cls.NONE


class Entity(ABC):
    def __init__(
        self,
        pixel_x: int,
        pixel_y: int
    ) -> None:
        """Store the entity's current, spawn and origin pixel positions."""
        self.pixel_x: int = pixel_x
        self.pixel_y: int = pixel_y
        self.spawn_pixel_x: int = pixel_x
        self.spawn_pixel_y: int = pixel_y
        self.origin_pixel_x: int = pixel_x
        self.origin_pixel_y: int = pixel_y

    @abstractmethod
    def draw(
        self,
        screen: pygame.Surface
    ) -> None:
        """Draw the entity onto ``screen`` (implemented by subclasses)."""
        pass

    def is_aligned(
            self,
    ) -> bool:
        """Return whether the entity sits exactly on the maze grid."""
        return (
            (self.pixel_x - self.origin_pixel_x) % constant.WALL_HEIGHT == 0
            and (self.pixel_y - self.origin_pixel_y) %
            constant.WALL_HEIGHT == 0
        )
