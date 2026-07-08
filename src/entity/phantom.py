from ..strategies import Strategy, RetreatStrategy
from .entity import Entity
from enum import Enum
from typing import Generator
from ..utils import Converter
import os
import pygame
from .. import constant


class ErrorPhant(Exception):
    def __init__(self, *args: str):
        super().__init__(*args)


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
            conv: Converter
    ):
        super().__init__(x, y)
        if not isinstance(strategy, Strategy):
            raise TypeError(f"Not a valid strategy: {strategy}")
        if color not in PhantomColor.ALL_COLORS.value:
            raise ValueError("Phantom is not a color that is supported")
        self.strategy: Strategy = strategy
        self.original_strategy: Strategy = strategy
        self.color: str = color
        self.sprites_dimensions: list[tuple[int, int]] = []
        self.sprites: list[pygame.Surface] = self.get_sprites()
        self.sprite_index: int = 0
        self.maze_pos: tuple[int, int] = maze_pos
        self.spawn_maze_pos: tuple[int, int] = maze_pos
        self.next_maze_pos: tuple[int, int] = maze_pos
        self.conv: Converter = conv
        self.path: list[tuple[int, int]] = []
        self.retreat: bool = False
        self.update_hitbox(x, y)
        # print(self.conv.get_coord_sprite(self.sprites[self.sprite_index].get_size(), (x, y)))
        # print((x, y))

    def update_target_pos(self, pos: tuple[int, int]) -> None:
        self.target_maze_pos = pos

    def set_retreat_strategy(self) -> None:
        self.strategy = RetreatStrategy(self.strategy.map_grid)
        self.retreat = True
        # self.next_maze_pos = self.maze_pos
        self.start_time = pygame.time.get_ticks()
        # self.update_path()

    def gen_move(
        self,
        path: list[tuple[int, int]]
    ) -> Generator[tuple[int, int], None, None]:
        for pos in path:
            yield pos
        return None

    def update_path(self) -> None:
        tmp = self.strategy.movement(
            self.maze_pos
        )
        if tmp != self.path:
            self.path = tmp
            self.movements = self.gen_move(self.path)

    def update_hitbox(
            self,
            x: int,
            y: int
            ) -> None:
        w, h = self.sprites_dimensions[self.sprite_index]
        self.hitbox: pygame.Rect = pygame.Rect(
            x + w // 4,
            y + h // 4,
            w // 2,
            h // 2
        )

    def get_pxl_pos_delta(self, delta: float) -> int:
        if delta > 0:
            return 1
        elif delta < 0:
            return -1
        else:
            return 0

    def get_next_pos(self) -> tuple[int, int]:
        try:
            next_pos: tuple[int, int] = next(self.movements)
            return next_pos
        except StopIteration:
            raise ErrorPhant("No more movements available")

    # Base on strategy it will move differently from other phantoms
    # il faut remetre self.next_maze_pos
    def move(self):
        # print("current pos", self.maze_pos)
        # print("next pos", self.next_maze_pos)
        # print("x, y:", self.x, self.y)
        # print("path", self.path)
        if self.next_maze_pos == self.maze_pos:
            self.update_path()
            try:
                self.next_maze_pos = next(self.movements)
            except StopIteration:
                return
        next_pxl_coord = self.conv.maze_to_pxl(self.next_maze_pos)
        next_pxl_x, next_pxl_y = self.conv.get_coord_sprite(
            self.sprites_dimensions[self.sprite_index], next_pxl_coord)
        # print("next x y :", next_pxl_x, next_pxl_y)
        # if (self.x, self.y) == (next_pxl_x, next_pxl_y):
        #     self.maze_pos = self.next_maze_pos
        #     self.update_path()
        #     try:
        #         self.next_maze_pos = next(self.movements)
        #     except StopIteration:
        #         return

        #     try:
        #         self.next_maze_pos = self.get_next_pos()
        #     except ErrorPhant:
        #         self.update_path()
        #         self.next_maze_pos = self.get_next_pos()
        # print(self.next_maze_pos)
        next_pxl_x, next_pxl_y = self.conv.maze_to_pxl(self.next_maze_pos)
        self.update_hitbox(next_pxl_x, next_pxl_y)
        dx = next_pxl_x - self.x
        dy = next_pxl_y - self.y
        x = self.get_pxl_pos_delta(dx)
        y = self.get_pxl_pos_delta(dy)
        self.x += x
        self.y += y
        if (self.x, self.y) == (next_pxl_x, next_pxl_y):
            self.maze_pos = self.next_maze_pos
        # self.maze_pos = self.next_maze_pos
        # if (next_pxl_x, next_pxl_y) == (self.x, self.y):
        #   self.maze_pos = self.next_maze_pos
        # print(self.maze_pos)

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
                self.sprites_dimensions.append(sprites[-1].get_size())
        return sprites

    def draw(
        self,
        screen: pygame.Surface
    ) -> None:
        self.change_sprite()
        screen.blit(self.sprites[self.sprite_index], (self.x, self.y))

    def change_sprite(
        self
    ) -> None:
        ax, ay = self.maze_pos
        try:
            nx, ny = self.maze_pos
        except ErrorPhant:
            nx, ny = self.maze_pos
        if ay < ny:
            self.sprite_index = 1
        elif ay > ny:
            self.sprite_index = 2
        elif ax < nx:
            self.sprite_index = 3
        elif ax > nx:
            self.sprite_index = 0

    def update(
        self,
        player_pos
    ) -> None:
        if self.retreat:
            tick = pygame.time.get_ticks()
            if tick - self.start_time >= self.strategy.duration:
                self.retreat = False
                self.strategy = self.original_strategy
                # self.next_maze_pos = self.maze_pos
        Strategy.set_player_pos(player_pos)
        self.move()

    def reset_position(
        self
    ) -> None:
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.maze_pos = self.spawn_maze_pos
        self.strategy = self.original_strategy
        # self.next_maze_pos = self.maze_pos
        self.retreat = False
