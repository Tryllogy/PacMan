import pygame
import os
from .entity import Direction, Entity
from .. import constant


class Player(Entity):
    def __init__(
        self,
        x: int,
        y: int
    ) -> None:
        super().__init__(x, y)
        self.sprites: list[pygame.Surface] = self.get_sprites()
        self.sprite_index: int = 0
        self.current_sprite: pygame.Surface = self.sprites[self.sprite_index]
        self.direction: Direction = Direction.RIGHT
        self.points: int = 0

    def draw(
        self,
        screen
    ) -> None:
        self.current_sprite = pygame.transform.rotate(
            self.sprites[self.sprite_index],
            {
                Direction.UP: 90,
                Direction.DOWN: 270,
                Direction.LEFT: 180,
                Direction.RIGHT: 0
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
        return sprites

    def check_collision(
        self,
        x: int,
        y: int,
        entities: list[pygame.Rect]
    ) -> bool:
        player_rect: pygame.Rect = pygame.Rect(
            x,
            y,
            constant.WALL_HEIGHT - constant.WALL_WIDTH * 1.5,
            constant.WALL_HEIGHT - constant.WALL_WIDTH * 1.5
        )
        for entity in entities:
            if player_rect.colliderect(entity):
                return True
        return False

    def update(
        self,
        walls: list[pygame.Rect],
        pacgums: list[pygame.Rect] = [],
        super_pacgums: list[pygame.Rect] = []
    ) -> None:
        match self.direction:
            case Direction.UP:
                if not self.check_collision(
                        self.x, self.y - constant.PLAYER_SPEED, walls):
                    self.y -= constant.PLAYER_SPEED
            case Direction.DOWN:
                if not self.check_collision(
                        self.x, self.y + constant.PLAYER_SPEED, walls):
                    self.y += constant.PLAYER_SPEED
            case Direction.LEFT:
                if not self.check_collision(
                        self.x - constant.PLAYER_SPEED, self.y, walls):
                    self.x -= constant.PLAYER_SPEED
            case Direction.RIGHT:
                if not self.check_collision(
                        self.x + constant.PLAYER_SPEED, self.y, walls):
                    self.x += constant.PLAYER_SPEED
        if self.check_collision(self.x, self.y, pacgums):
            print("Pacgum collected!")
