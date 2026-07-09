import pygame
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
        x: int,
        y: int,
        origin_x: int,
        origin_y: int,
        score: Score,
        lives: int = 0,
        points_per_pacgum: int = 1,
        points_per_super_pacgum: int = 5,
        points_per_ghost: int = 10,
    ) -> None:
        super().__init__(x, y)
        self.origin_x: int = origin_x
        self.origin_y: int = origin_y
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

    # Sprites face right, every other direction is a rotation of them
    ROTATIONS: dict[Direction, int] = {
        Direction.UP: 90,
        Direction.DOWN: 270,
        Direction.LEFT: 180,
        Direction.RIGHT: 0,
        Direction.NONE: 0
    }

    def draw(
        self,
        screen
    ) -> None:
        sprite = pygame.transform.rotate(
            self.sprites.get(Direction.RIGHT, self.sprite_index),
            self.ROTATIONS[self.direction]
        )
        screen.blit(sprite, (self.x, self.y))

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
        x: int,
        y: int,
        entities: list[Wall | Pacgum | SuperPacgum]
    ) -> tuple[bool, Wall | Pacgum | SuperPacgum | None]:
        self.update_hitbox(x, y)
        for entity in entities:
            if self.hitbox.colliderect(entity.rect):
                return True, entity
        return False, None

    def check_collision_with_phantoms(
        self,
        x: int,
        y: int,
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
        dx, dy = {
            Direction.UP: (0, -constant.PLAYER_SPEED),
            Direction.DOWN: (0, constant.PLAYER_SPEED),
            Direction.LEFT: (-constant.PLAYER_SPEED, 0),
            Direction.RIGHT: (constant.PLAYER_SPEED, 0),
            Direction.NONE: (0, 0)
        }[direction]
        new_x:  int = self.x + dx * 2
        new_y:  int = self.y + dy * 2
        return not self.check_collision(new_x, new_y, walls)[0]

    def update(
        self,
        walls: list[Wall],
        pacgums: list[Pacgum] = [],
        super_pacgums: list[SuperPacgum] = [],
        phantoms: list[Phantom] = []
    ) -> None:
        self.update_hitbox(self.x, self.y)
        if self.is_aligned() and self.can_move(walls, self.next_direction):
            self.direction = self.next_direction
        if self.can_move(walls, self.direction):
            dx, dy = {
                Direction.UP: (0, -constant.PLAYER_SPEED),
                Direction.DOWN: (0, constant.PLAYER_SPEED),
                Direction.LEFT: (-constant.PLAYER_SPEED, 0),
                Direction.RIGHT: (constant.PLAYER_SPEED, 0),
                Direction.NONE: (0, 0)
            }[self.direction]
            self.x += dx
            self.y += dy
        self.update_sprite()
        if self.check_collision(self.x, self.y, pacgums)[0]:
            self.score.score += self.points_per_pacgum
            pacgums.remove(self.check_collision(self.x, self.y, pacgums)[1])
        if self.check_collision(self.x, self.y, super_pacgums)[0]:
            self.score.score += self.points_per_super_pacgum
            super_pacgums.remove(self.check_collision(self.x, self.y,
                                                      super_pacgums)[1])
            for phantom in phantoms:
                phantom.set_retreat_strategy()
        collision_with_phantom, phantom = self.check_collision_with_phantoms(
            self.x, self.y, phantoms)
        if collision_with_phantom:
            if phantom.retreat:
                phantom.set_spawn_strategy()
                self.score.score += self.points_per_ghost
            elif not phantom.retreat and not phantom.to_spawn:
                self.lives -= 1
                self.reset_positions()
                for phantom in phantoms:
                    phantom.reset_position()

    def reset_positions(
        self,
    ) -> None:
        self.x = self.spawn_x
        self.y = self.spawn_y
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
        x: int,
        y: int
    ) -> None:
        w, h = self.sprites.size(Direction.RIGHT, self.sprite_index)
        self.hitbox: pygame.Rect = pygame.Rect(x, y, w, h)
