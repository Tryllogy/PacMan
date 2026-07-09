from ..strategies import (Strategy, RetreatStrategy,
                          ReturnToSpawnStrategy)
from .entity import Entity, Direction
from .sprite import SpriteSet, load_scaled
from enum import Enum
from typing import Generator
from ..utils import Converter
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
            conv: Converter
    ):
        super().__init__(x, y)
        if not isinstance(strategy, Strategy):
            raise TypeError(f"Not a valid strategy: {strategy}")
        if color not in PhantomColor.ALL_COLORS.value:
            raise ValueError("Phantom is not a color that is supported")
        self.strategy: Strategy = strategy
        self.original_strategy: Strategy = strategy
        self.retreat_strategy = RetreatStrategy(self.strategy.map_grid)
        self.color: str = color
        self.direction: Direction = Direction.LEFT
        self.sprites: SpriteSet
        self.dead_sprites: SpriteSet
        self.sprites, self.dead_sprites = self.load_sprites()
        self.scared_sprite: pygame.Surface = load_scaled("scared_ghost.png")
        self.prev_pos: tuple[int, int] = maze_pos
        self.maze_pos: tuple[int, int] = maze_pos
        self.next_maze_pos: tuple[int, int] = maze_pos
        self.spawn_maze_pos: tuple[int, int] = maze_pos
        self.conv: Converter = conv
        self.path: list[tuple[int, int]] = []
        self.retreat: bool = False
        self.to_spawn: bool = False
        self.update_hitbox(x, y)
        self.retreat_timer = constant.RETREAT_TIME
        self.respawn_timer: int = constant.RESPAWN_TIME
        self.spawn_strategy: Strategy = ReturnToSpawnStrategy(
            self.strategy.map_grid, maze_pos)
        pygame.time.set_timer(pygame.USEREVENT + 2, 1000)

    def set_retreat_strategy(self) -> None:
        if not self.retreat:
            self.strategy = self.retreat_strategy
            self.retreat = True
        self.retreat_timer = constant.RETREAT_TIME

    def set_spawn_strategy(self) -> None:
        self.strategy = self.spawn_strategy
        self.next_maze_pos = self.maze_pos
        self.retreat = False
        self.to_spawn = True
        self.respawn_timer = constant.RESPAWN_TIME

    def gen_move(
        self,
        path: list[tuple[int, int]]
    ) -> Generator[tuple[int, int], None, None]:
        for pos in path:
            yield pos
        return None

    def update_path(self, player_pos: tuple[int, int]) -> None:
        tmp = self.strategy.movement(self.maze_pos, player_pos, self.prev_pos)
        if len(tmp) > 0 and tmp[0] == self.maze_pos:
            tmp.pop(0)
        self.path = tmp
        self.movements = self.gen_move(self.path)

    def update_hitbox(
            self,
            x: int,
            y: int
    ) -> None:
        w, h = self.sprites.size(self.direction)
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

    # Base on strategy it will move differently from other phantoms
    def move(self, player_pos: tuple[int, int]):
        if self.next_maze_pos == self.maze_pos:
            self.update_path(player_pos)
            try:
                self.next_maze_pos = next(self.movements)
            except StopIteration:
                return
            direction = Direction.from_maze_delta(
                self.maze_pos, self.next_maze_pos)
            if direction != Direction.NONE:
                self.direction = direction
        next_pxl_x, next_pxl_y = self.conv.maze_to_pxl(self.next_maze_pos)
        self.update_hitbox(next_pxl_x, next_pxl_y)
        dx = next_pxl_x - self.x
        dy = next_pxl_y - self.y
        x = self.get_pxl_pos_delta(dx)
        y = self.get_pxl_pos_delta(dy)
        self.x += x
        self.y += y
        if (self.x, self.y) == (next_pxl_x, next_pxl_y):
            self.prev_pos = self.maze_pos
            self.maze_pos = self.next_maze_pos

    def load_sprites(
        self
    ) -> tuple[SpriteSet, SpriteSet]:
        colored_sprites = SpriteSet({
            Direction.UP: [load_scaled(f"{self.color}_ghost_top.png")],
            Direction.DOWN: [load_scaled(f"{self.color}_ghost_bot.png")],
            Direction.LEFT: [load_scaled(f"{self.color}_ghost_left.png")],
            Direction.RIGHT: [load_scaled(f"{self.color}_ghost_right.png")],
        })
        dead_sprites = SpriteSet({
            Direction.UP: [load_scaled("dead_ghost_top.png")],
            Direction.DOWN: [load_scaled("dead_ghost_bot.png")],
            Direction.LEFT: [load_scaled("dead_ghost_left.png")],
            Direction.RIGHT: [load_scaled("dead_ghost_right.png")],
        })
        return colored_sprites, dead_sprites

    def draw(
        self,
        screen: pygame.Surface
    ) -> None:
        if self.retreat:
            screen.blit(self.scared_sprite, (self.x, self.y))
        elif self.to_spawn:
            screen.blit(self.dead_sprites.get(
                self.direction), (self.x, self.y))
        else:
            screen.blit(self.sprites.get(self.direction), (self.x, self.y))

    def update(
        self,
        player_pos
    ) -> None:
        if self.to_spawn and self.maze_pos == self.spawn_maze_pos:
            self.to_spawn = False
            self.strategy = self.original_strategy
        self.move(player_pos)

    def reset_strategy(self):
        self.strategy = self.original_strategy
        self.retreat = False
        self.to_spawn = False

    def reset_position(
        self
    ) -> None:
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.maze_pos = self.spawn_maze_pos
        self.strategy = self.original_strategy
        self.next_maze_pos = self.maze_pos
        self.direction = Direction.LEFT
        self.retreat = False
        self.to_spawn = False
