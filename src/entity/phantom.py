from ..strategies import Strategy
from .entity import Entity, Direction
from enum import Enum
from typing import Generator
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


class Phantom(Entity):
    def __init__(
            self,
            x: int,
            y: int,
            strategy: Strategy,
            color: str,
            maze_pos: tuple[int, int],
            ppc: tuple[int, int],
            offset: tuple[int, int]
    ):
        super().__init__(x, y)
        if not isinstance(strategy, Strategy):
            raise TypeError(f"Not a valid strategy: {strategy}")
        if color not in PhantomColor.ALL_COLORS.value:
            raise ValueError("Phantom is not a color that is supported")
        self.strategy: Strategy = strategy
        self.color: str = color
        self.sprites: list[pygame.Surface] = self.get_sprites()
        self.sprite_index: int = 0
        self.current_sprite: pygame.Surface = self.sprites[self.sprite_index]
        self.direction: Direction = Direction.RIGHT
        self.maze_pos: tuple[int, int] = maze_pos
        self.ppc: tuple[int, int] = ppc
        self.offset: tuple[int, int] = offset
        # self.ppc_w: int = ppc_w
        # self.ppc_h: int = ppc_h
        self.path: list[tuple[int, int]] = []
        self.hitbox: pygame.Rect

    def update_player_pos(self, pos: tuple[int, int]) -> None:
        self.player_maze_pos = pos

    def change_strategy(
            self,
            strategy: Strategy
    ):
        if not isinstance(strategy, Strategy):
            raise TypeError(f"Not a valid strategy: {strategy}")
        self.strategy = strategy

    def gen_move(
        self,
        path: list[tuple[int, int]]
    ) -> Generator[tuple[int, int], None, None]:
        for pos in path:
            yield pos
        return None

    def update_path(self) -> None:
        self.path = self.strategy.movement(
            self.maze_pos,
            self.player_maze_pos
        )
        self.movements = self.gen_move(self.path)

    def update_hitbox(
            self,
            x: int,
            y: int
            ) -> None:
        w, h = self.current_sprite.get_size()
        self.hitbox: pygame.Rect = pygame.Rect(
            x,
            y,
            w,
            h
        )

    # Base on strategy it will move differently from other phantoms
    def move(self):
        try:
            case_x, case_y = next(self.movements)
        except StopIteration:
            return
        pxl_x = case_x * self.ppc[0] + self.offset[0]
        pxl_y = case_y * self.ppc[1] + self.offset[1]
        self.update_hitbox(pxl_x, pxl_y)  # convert x, y in pxl from screen. self.movements give position in maze case x, y

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
                    (constant.WALL_HEIGHT - constant.WALL_WIDTH * 1.5,
                     constant.WALL_HEIGHT - constant.WALL_WIDTH * 1.5))
        return sprites

    def draw(
        self,
        screen: pygame.Surface
    ) -> None:
        self.change_sprite()
        screen.blit(self.current_sprite, (self.x, self.y))

    def change_sprite(
        self
    ) -> None:
        if self.direction == Direction.DOWN:
            self.sprite_index = 0
        elif self.direction == Direction.LEFT:
            self.sprite_index = 1
        elif self.direction == Direction.RIGHT:
            self.sprite_index = 2
        elif self.direction == Direction.UP:
            self.sprite_index = 3

    def update(
        self,
        player_pos
    ) -> None:
        self.update_player_pos(player_pos)
        self.update_path()
        self.move()

    def reset_position(
        self
    ) -> None:
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.maze_pos = (self.spawn_x // self.ppc[0],
                         self.spawn_y // self.ppc[1])
