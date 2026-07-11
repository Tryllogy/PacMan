import pygame
from collections.abc import Sequence
from .entity import Direction, Entity
from .sprite import SpriteSet, load_scaled
from .phantom import Phantom
from .wall import Wall
from .pacgum import Pacgum
from .superpacgum import SuperPacgum
from .score import Score
from .. import constant


class Player(Entity):
    def __init__(
        self,
        pixel_x: int,
        pixel_y: int,
        origin_pixel_x: int,
        origin_pixel_y: int,
        score: Score,
        lives: int = 0,
        points_per_pacgum: int = 1,
        points_per_super_pacgum: int = 5,
        points_per_ghost: int = 10,
    ) -> None:
        super().__init__(pixel_x, pixel_y)
        self.origin_pixel_x: int = origin_pixel_x
        self.origin_pixel_y: int = origin_pixel_y
        self.lives: int = lives
        self.points_per_pacgum: int = points_per_pacgum
        self.points_per_super_pacgum: int = points_per_super_pacgum
        self.points_per_ghost: int = points_per_ghost
        self.score: Score = score
        self.sprite_index: int = 0
        self.sprites: SpriteSet = self.get_sprites()
        self.last_sprite_change_time: int = pygame.time.get_ticks()
        self.direction: Direction = Direction.NONE
        self.next_direction: Direction = self.direction
        self.hitbox: pygame.Rect
        self.invincible: bool = False

    ROTATIONS: dict[Direction, int] = {
        Direction.UP: 90,
        Direction.DOWN: 270,
        Direction.LEFT: 180,
        Direction.RIGHT: 0,
        Direction.NONE: 0
    }

    def draw(
        self,
        screen: pygame.Surface
    ) -> None:
        sprite = pygame.transform.rotate(
            self.sprites.get(Direction.RIGHT, self.sprite_index),
            self.ROTATIONS[self.direction]
        )
        screen.blit(sprite, (self.pixel_x, self.pixel_y))

    def get_sprites(
        self
    ) -> SpriteSet:
        return SpriteSet({
            Direction.RIGHT: [
                load_scaled("pacman_1.png"),
                load_scaled("pacman_2.png"),
                load_scaled("pacman_3.png"),
            ]
        })

    def check_collision(
        self,
        pixel_x: int,
        pixel_y: int,
        entities: Sequence[Wall | Pacgum | SuperPacgum]
    ) -> tuple[bool, Wall | Pacgum | SuperPacgum | None]:
        self.update_hitbox(pixel_x, pixel_y)
        for entity in entities:
            if self.hitbox.colliderect(entity.rect):
                return True, entity
        return False, None

    def check_collision_with_phantoms(
        self,
        pixel_x: int,
        pixel_y: int,
        phantoms: list[Phantom]
    ) -> tuple[bool, Phantom | None]:
        if self.invincible:
            return False, None
        for phantom in phantoms:
            if phantom.to_spawn:
                continue
            if self.hitbox.colliderect(phantom.hitbox):
                return True, phantom
        return False, None

    def can_move(
        self,
        walls: list[Wall],
        direction: Direction
    ) -> bool:
        d_pixel_x, d_pixel_y = {
            Direction.UP: (0, -constant.PLAYER_SPEED),
            Direction.DOWN: (0, constant.PLAYER_SPEED),
            Direction.LEFT: (-constant.PLAYER_SPEED, 0),
            Direction.RIGHT: (constant.PLAYER_SPEED, 0),
            Direction.NONE: (0, 0)
        }[direction]
        new_pixel_x: int = self.pixel_x + d_pixel_x * 2
        new_pixel_y: int = self.pixel_y + d_pixel_y * 2
        return not self.check_collision(new_pixel_x, new_pixel_y, walls)[0]

    def update(
        self,
        walls: list[Wall],
        pacgums: list[Pacgum] = [],
        super_pacgums: list[SuperPacgum] = [],
        phantoms: list[Phantom] = []
    ) -> None:
        if self.is_aligned() and self.can_move(walls, self.next_direction):
            self.direction = self.next_direction
        if self.can_move(walls, self.direction):
            d_pixel_x, d_pixel_y = {
                Direction.UP: (0, -constant.PLAYER_SPEED),
                Direction.DOWN: (0, constant.PLAYER_SPEED),
                Direction.LEFT: (-constant.PLAYER_SPEED, 0),
                Direction.RIGHT: (constant.PLAYER_SPEED, 0),
                Direction.NONE: (0, 0)
            }[self.direction]
            self.pixel_x += d_pixel_x
            self.pixel_y += d_pixel_y
        self.update_hitbox(self.pixel_x, self.pixel_y)
        self.update_sprite()
        hit_pacgum, pacgum = self.check_collision(
            self.pixel_x, self.pixel_y, pacgums)
        if hit_pacgum and isinstance(pacgum, Pacgum):
            self.score.score += self.points_per_pacgum
            pacgums.remove(pacgum)
        hit_super, super_pacgum = self.check_collision(
            self.pixel_x, self.pixel_y, super_pacgums)
        if hit_super and isinstance(super_pacgum, SuperPacgum):
            self.score.score += self.points_per_super_pacgum
            super_pacgums.remove(super_pacgum)
            for phantom in phantoms:
                phantom.set_retreat_strategy()
        collided, hit_phantom = self.check_collision_with_phantoms(
            self.pixel_x, self.pixel_y, phantoms)
        if collided and hit_phantom is not None:
            if hit_phantom.retreat:
                hit_phantom.set_spawn_strategy()
                self.score.score += self.points_per_ghost
            elif not hit_phantom.retreat and not hit_phantom.to_spawn:
                self.lives -= 1
                self.reset_positions()
                for phantom in phantoms:
                    phantom.reset_position()

    def reset_positions(
        self,
    ) -> None:
        self.pixel_x = self.spawn_pixel_x
        self.pixel_y = self.spawn_pixel_y
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE
        self.sprite_index = 0

    def update_sprite(
        self,
    ) -> None:
        now: int = pygame.time.get_ticks()
        if now - self.last_sprite_change_time >= \
                constant.PLAYER_SPRITE_CHANGE_DELAY:
            self.last_sprite_change_time = now
            self.sprite_index = (self.sprite_index + 1) % \
                self.sprites.frame_count(Direction.RIGHT)

    def update_hitbox(
        self,
        pixel_x: int,
        pixel_y: int
    ) -> None:
        w, h = self.sprites.size(self.direction, self.sprite_index)
        self.hitbox = pygame.Rect(
            pixel_x,
            pixel_y,
            w,
            h
        )
