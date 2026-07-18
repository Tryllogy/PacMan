from ..strategies import (Strategy, RetreatStrategy,
                          ReturnToSpawnStrategy)
from .entity import Entity, Direction
from .sprite import SpriteSet, load_scaled
from enum import Enum
from typing import Generator
from ..utils import Converter
from ..graphics import Surface, Rect, get_ticks
from .. import constant


class PhantomColor(Enum):
    PURPLE = "purple"
    BLUE = "blue"
    GREEN = "green"
    RED = "red"

    ALL_COLORS = [
        PURPLE,
        BLUE,
        GREEN,
        RED
    ]


class Phantom(Entity):
    def __init__(
            self,
            pixel_x: int,
            pixel_y: int,
            strategy: Strategy,
            color: str,
            cell: tuple[int, int],
            conv: Converter
    ):
        super().__init__(pixel_x, pixel_y)
        if not isinstance(strategy, Strategy):
            raise TypeError(f"Not a valid strategy: {strategy}")
        if color not in PhantomColor.ALL_COLORS.value:
            raise ValueError("Phantom is not a color that is supported")
        self.color: str = color
        self.conv: Converter = conv
        self.strategy: Strategy = strategy
        self.original_strategy: Strategy = strategy
        self.spawn_strategy: Strategy = ReturnToSpawnStrategy(
            self.strategy.map_grid, cell)
        self.retreat_strategy = RetreatStrategy(self.strategy.map_grid)
        self.direction: Direction = Direction.LEFT
        self.sprites: SpriteSet
        self.dead_sprites: SpriteSet
        self.scared_sprite: list[Surface]
        self.sprites, \
            self.dead_sprites, \
            self.scared_sprite = self.load_sprites()
        self.scared_sprite_index: int = 0
        self.last_sprite_change_time: int = get_ticks()
        self.prev_cell: tuple[int, int] = cell
        self.cell: tuple[int, int] = cell
        self.next_cell: tuple[int, int] = cell
        self.spawn_cell: tuple[int, int] = cell
        self.path: list[tuple[int, int]] = []
        self.retreat_timer = constant.RETREAT_TIME
        self.respawn_timer: int = constant.RESPAWN_TIME
        self.update_hitbox(pixel_x, pixel_y)

    @property
    def retreat(self) -> bool:
        return isinstance(self.strategy, RetreatStrategy)

    @property
    def to_spawn(self) -> bool:
        return isinstance(self.strategy, ReturnToSpawnStrategy)

    def set_retreat_strategy(self) -> None:
        if self.to_spawn:
            return
        self.strategy = self.retreat_strategy
        self.retreat_timer = constant.RETREAT_TIME
        self.last_sprite_change_time = get_ticks()

    def set_spawn_strategy(self) -> None:
        self.strategy = self.spawn_strategy
        self.respawn_timer = constant.RESPAWN_TIME

    def gen_move(
        self,
        path: list[tuple[int, int]]
    ) -> Generator[tuple[int, int], None, None]:
        for cell in path:
            yield cell
        return None

    def update_path(self, player_cell: tuple[int, int]) -> None:
        tmp = self.strategy.movement(self.cell, player_cell, self.prev_cell)
        if len(tmp) > 0 and tmp[0] == self.cell:
            tmp.pop(0)
        self.path = tmp
        self.movements = self.gen_move(self.path)

    def update_hitbox(
            self,
            pixel_x: int,
            pixel_y: int
    ) -> None:
        w, h = self.sprites.size(self.direction)
        self.hitbox: Rect = Rect(
            pixel_x,
            pixel_y,
            w,
            h
        )

    def get_pixel_delta(self, delta: float) -> int:
        if delta > 0:
            return 1
        elif delta < 0:
            return -1
        else:
            return 0

    def move(self, player_cell: tuple[int, int]) -> None:
        if self.next_cell == self.cell:
            self.update_path(player_cell)
            try:
                self.next_cell = next(self.movements)
            except StopIteration:
                return
            direction = Direction.from_cell_delta(self.cell, self.next_cell)
            if direction != Direction.NONE:
                self.direction = direction
        next_pixel_x, next_pixel_y = self.conv.cell_to_pixel(self.next_cell)
        self.pixel_x += self.get_pixel_delta(next_pixel_x - self.pixel_x)
        self.pixel_y += self.get_pixel_delta(next_pixel_y - self.pixel_y)
        if (self.pixel_x, self.pixel_y) == (next_pixel_x, next_pixel_y):
            self.prev_cell = self.cell
            self.cell = self.next_cell

    def load_sprites(
        self
    ) -> tuple[SpriteSet, SpriteSet, list[Surface]]:
        try:
            colored_sprites = SpriteSet({
                Direction.UP: [load_scaled(f"{self.color}_ghost_top.png")],
                Direction.DOWN: [load_scaled(f"{self.color}_ghost_bot.png")],
                Direction.LEFT: [load_scaled(f"{self.color}_ghost_left.png")],
                Direction.RIGHT:
                [load_scaled(f"{self.color}_ghost_right.png")],
            })
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Sprites for color {self.color} not "
                f"found in the sprite directory"
                "Must be named as <color>_ghost_<direction>.png")
        try:
            dead_sprites = SpriteSet({
                Direction.UP: [load_scaled("dead_ghost_top.png")],
                Direction.DOWN: [load_scaled("dead_ghost_bot.png")],
                Direction.LEFT: [load_scaled("dead_ghost_left.png")],
                Direction.RIGHT: [load_scaled("dead_ghost_right.png")],
            })
        except FileNotFoundError:
            raise FileNotFoundError(
                "Dead ghost sprites not found in the sprite directory"
                "Must be named as dead_ghost_<direction>.png")
        try:
            scared_sprite = [load_scaled("scared_ghost_1.png"),
                             load_scaled("scared_ghost_2.png")]
        except FileNotFoundError:
            raise FileNotFoundError(
                "Scared ghost sprite not found in the sprite directory"
                "Must be named as scared_ghost_<number>.png")
        return colored_sprites, dead_sprites, scared_sprite

    def draw(
        self,
        screen: Surface
    ) -> None:
        if self.retreat:
            now = get_ticks()
            if (self.retreat_timer < 3 and
                    now - self.last_sprite_change_time >=
                    constant.GHOST_SPRITE_CHANGE_DELAY):
                self.last_sprite_change_time = now
                self.scared_sprite_index = (
                    self.scared_sprite_index + 1) % len(self.scared_sprite)
            screen.blit(
                self.scared_sprite[self.scared_sprite_index],
                (self.pixel_x, self.pixel_y))
        elif self.to_spawn:
            screen.blit(self.dead_sprites.get(
                self.direction), (self.pixel_x, self.pixel_y))
        else:
            screen.blit(self.sprites.get(
                self.direction), (self.pixel_x, self.pixel_y))

    def update(
        self,
        player_cell: tuple[int, int]
    ) -> None:
        self.update_hitbox(self.pixel_x, self.pixel_y)
        if self.to_spawn and self.cell == self.spawn_cell:
            self.strategy = self.original_strategy
        self.move(player_cell)

    def reset_strategy(self) -> None:
        self.strategy = self.original_strategy
        self.scared_sprite_index = 0

    def reset_position(
        self
    ) -> None:
        self.pixel_x = self.spawn_pixel_x
        self.pixel_y = self.spawn_pixel_y
        self.cell = self.spawn_cell
        self.next_cell = self.cell
        self.direction = Direction.LEFT
        self.reset_strategy()
