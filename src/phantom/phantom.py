from ..strategies import Strategy
from enum import Enum
import os
import pygame
from .. import constant


class PhantomColor(Enum):
    PURPLE: str = "purple"
    BLUE: str = "blue"
    GREEN: str = "green"
    RED: str = "red"

    ALL_COLORS: list[str] = [
        PURPLE,
        BLUE,
        GREEN,
        RED
    ]


class Phantom:
    def __init__(
            self,
            x: int,
            y: int,
            strategy: Strategy,
            color: str,
    ):
        self.x: int = x
        self.y: int = y
        if color not in PhantomColor.ALL_COLORS.value:
            raise ValueError("Phantom is not a color that is supported")
        self.strategy: Strategy = strategy
        self.color: str = color
        self.sprites: list = self.get_sprites()
        self.sprite_index: int = 0

    def change_strategy(
            self,
            strategy: Strategy
    ):
        if not isinstance(strategy, Strategy):
            raise TypeError(f"Not a valid strategy: {strategy}")
        self.strategy = strategy

    # Base on strategy it will move differently from other phantoms
    def move(self):
        pass

    def get_sprites(
        self
    ) -> list[pygame.Surface]:
        sprites: list[pygame.Surface] = []
        sprite_dir: str = os.path.join("src/sprites")
        all_sprites_str = os.listdir(sprite_dir)
        for sprite in all_sprites_str:
            if self.color in sprite:
                sprites.append(
                    pygame.image.load(os.path.join(sprite_dir, sprite)))
                sprites[-1] = pygame.transform.scale(
                    sprites[-1],
                    (constant.WALL_HEIGHT - constant.WALL_WIDTH,
                     constant.WALL_HEIGHT - constant.WALL_WIDTH))
        return sprites

    def draw(
        self,
        screen: pygame.Surface
    ) -> None:
        screen.blit(self.sprites[self.sprite_index], (self.x, self.y))
