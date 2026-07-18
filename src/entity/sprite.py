from .entity import Direction
from .. import constant
from ..graphics import Surface, load_image, scale
from ..graphics.app import app
import os


def load_scaled(filename: str) -> Surface:
    size = int(constant.WALL_HEIGHT - constant.WALL_WIDTH * 1.5)
    image = load_image(app, os.path.join(constant.SPRITE_DIR, filename))
    return scale(image, (size, size))


class SpriteSet():
    def __init__(
        self,
        frames: dict[Direction, list[Surface]]
    ) -> None:
        if not frames:
            raise ValueError("A SpriteSet needs at least one direction")
        self.frames: dict[Direction, list[Surface]] = frames
        self.default: list[Surface] = next(iter(frames.values()))

    def get(
        self,
        direction: Direction,
        frame: int = 0
    ) -> Surface:
        images = self.frames.get(direction, self.default)
        return images[frame % len(images)]

    def size(
        self,
        direction: Direction,
        frame: int = 0
    ) -> tuple[int, int]:
        width, height = self.get(direction, frame).get_size()
        return (int(width), int(height))

    def frame_count(
        self,
        direction: Direction
    ) -> int:
        return len(self.frames.get(direction, self.default))
