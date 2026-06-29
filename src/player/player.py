import pygame
import os
from .. import constant


class Player:
    def __init__(
        self,
        x: int,
        y: int
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.spawn_x: int = x
        self.spawn_y: int = y
        self.sprites: list[pygame.Surface] = self.get_sprites()

    def draw(
        self,
        screen
    ) -> None:
        screen.blit(self.sprites[0], (self.x, self.y))

    def get_sprites(
        self
    ) -> list[pygame.Surface]:
        sprites: list[pygame.Surface] = []
        sprite_dir: str = os.path.join("src/sprites")
        all_sprites_str = os.listdir(sprite_dir)
        for sprite in all_sprites_str:
            if "pacman" in sprite:
                sprites.append(
                    pygame.image.load(os.path.join(sprite_dir, sprite)))
                sprites[-1] = pygame.transform.scale(
                    sprites[-1],
                    (constant.WALL_HEIGHT - constant.WALL_WIDTH * 1.5,
                     constant.WALL_HEIGHT - constant.WALL_WIDTH * 1.5))
        return sprites
