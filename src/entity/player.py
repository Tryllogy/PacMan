import pygame
import os
from .entity import Direction, Entity
from .phantom import Phantom
from .wall import Wall
from .pacgum import Pacgum
from .superpacgum import SuperPacgum
from .. import constant


class Player(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        origin_x: int,
        origin_y: int,
        lives: int,
        points_per_pacgum: int = 1,
        points_per_super_pacgum: int = 5,
        points_per_ghost: int = 10
    ) -> None:
        super().__init__(x, y)
        self.origin_x: int = origin_x
        self.origin_y: int = origin_y
        self.lives: int = lives
        self.points_per_pacgum: int = points_per_pacgum
        self.points_per_super_pacgum: int = points_per_super_pacgum
        self.points_per_ghost: int = points_per_ghost
        self.points: int = 0
        self.sprite_dimensions: list[tuple[int, int]] = []
        self.sprite_index: int = 0
        self.sprites: list[pygame.Surface] = self.get_sprites()
        self.current_sprite: pygame.Surface = self.sprites[self.sprite_index]
        self.direction: Direction = Direction.NONE
        self.next_direction: Direction = self.direction
        self.hitbox: pygame.Rect
        self.invincible: bool = False

    def draw(
        self,
        screen
    ) -> None:
        if self.direction == Direction.NONE:
            screen.blit(self.current_sprite, (self.x, self.y))
            return
        self.current_sprite = pygame.transform.rotate(
            self.sprites[self.sprite_index],
            {
                Direction.UP: 90,
                Direction.DOWN: 270,
                Direction.LEFT: 180,
                Direction.RIGHT: 0,
                Direction.NONE: 0
            }[self.direction]
        )
        screen.blit(self.current_sprite, (self.x, self.y))

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
                self.sprite_dimensions.append(sprites[-1].get_size())
        return sprites

    def check_collision(
        self,
        x: int,
        y: int,
        entities: list[pygame.Rect]
    ) -> tuple[bool, pygame.Rect | None]:
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
    ) -> tuple[bool, pygame.Rect | None]:
        if self.invincible:
            return False, None
        self.update_hitbox(x, y)
        for phantom in phantoms:
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
            self.update_sprite()
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
        if self.check_collision(self.x, self.y, pacgums)[0]:
            self.points += self.points_per_pacgum
            pacgums.remove(self.check_collision(self.x, self.y, pacgums)[1])
        if self.check_collision(self.x, self.y, super_pacgums)[0]:
            self.points += self.points_per_super_pacgum
            super_pacgums.remove(self.check_collision(self.x, self.y,
                                                      super_pacgums)[1])
        if self.check_collision_with_phantoms(self.x, self.y, phantoms)[0]:
            self.lives -= 1
            self.x = self.spawn_x
            self.y = self.spawn_y
            self.direction = Direction.NONE
            self.next_direction = Direction.NONE

    def reset_positions(
        self,
        phantoms: list[Phantom]
    ) -> None:
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE
        for phantom in phantoms:
            phantom.reset_position()

    def update_sprite(
        self
    ) -> None:
        self.sprite_index += 1
        if self.sprite_index >= len(self.sprites):
            self.sprite_index = 0

    def update_hitbox(
        self,
        x: int,
        y: int
    ) -> None:
        self.hitbox: pygame.Rect = pygame.Rect(
            x,
            y,
            self.sprite_dimensions[self.sprite_index][0],
            self.sprite_dimensions[self.sprite_index][1]
        )
