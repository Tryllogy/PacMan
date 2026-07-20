from .entity import Direction
from .. import constant
import os
import pygame


def load_scaled(filename: str) -> pygame.Surface:
    """Load a sprite file and scale it to the standard entity size."""
    size = constant.WALL_HEIGHT - constant.WALL_WIDTH * 1.5
    image = pygame.image.load(os.path.join(constant.SPRITE_DIR, filename))
    return pygame.transform.scale(image, (size, size))


class SpriteSet():
    def __init__(
        self,
        frames: dict[Direction, list[pygame.Surface]]
    ) -> None:
        """Store the per-direction frames, using the first as the default."""
        if not frames:
            raise ValueError("A SpriteSet needs at least one direction")
        self.frames: dict[Direction, list[pygame.Surface]] = frames
        self.default: list[pygame.Surface] = next(iter(frames.values()))

    def get(
        self,
        direction: Direction,
        frame: int = 0
    ) -> pygame.Surface:
        """Return the surface for ``direction`` at ``frame`` (wraps around)."""
        images = self.frames.get(direction, self.default)
        return images[frame % len(images)]

    def size(
        self,
        direction: Direction,
        frame: int = 0
    ) -> tuple[int, int]:
        """Return the ``(width, height)`` of the given direction/frame."""
        width, height = self.get(direction, frame).get_size()
        return (int(width), int(height))

    def frame_count(
        self,
        direction: Direction
    ) -> int:
        """Return how many animation frames ``direction`` has."""
        return len(self.frames.get(direction, self.default))
