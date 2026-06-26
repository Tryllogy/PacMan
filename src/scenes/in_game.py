from .scene import Scene, GameState
import pygame
from enum import Enum
from mazegenerator import MazeGenerator
from ..phantom import Phantom
from ..player import Player
from .. import constant


class Walls(Enum):
    N: int = 1
    E: int = 2
    S: int = 4
    W: int = 8


class InGameScene(Scene):
    def __init__(
        self,
        screen: pygame.Surface,
        maze_gen: MazeGenerator
    ) -> None:
        super().__init__(screen)
        self.current_scene = GameState.GAME.value
        mx, my = self.middle_screen
        self.maze_gen: MazeGenerator = maze_gen
        self.phantoms: list[Phantom] = []
        self.player: Player = None
        self.cheat_invicible: bool = False

    def handle_events(
        self,
        events
    ) -> str:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                print("PAUSE")
        return self.current_scene

    def draw(
        self,
    ) -> None:
        super().draw()
        for x, line in enumerate(self.maze_gen.maze):
            for y, value in enumerate(line):
                self.make_wall(value, (x, y))

    def make_wall(
        self,
        value: int,
        pos: tuple[int, int]
    ):
        if value >> 3 & 1:
            self.draw_west(pos)
        if value >> 2 & 1:
            self.draw_south(pos)
        if value >> 1 & 1:
            self.draw_east(pos)
        if value & 1:
            self.draw_north(pos)

    def draw_north(
        self,
        pos: tuple[int, int],
    ) -> None:
        pos_x: int = pos[0] * constant.WALL_WIDTH
        pos_y: int = pos[1] * constant.WALL_HEIGHT
        pygame.draw.rect(
            self.screen,
            constant.WALL_COLOR,
            pygame.Rect(
                pos_x,
                pos_y,
                constant.WALL_HEIGHT,
                constant.WALL_WIDTH,
             ),
        )

    def draw_south(
        self,
        pos: tuple[int, int]
    ) -> None:
        pos_x: int = pos[0] * constant.WALL_WIDTH
        pos_y: int = pos[1] * constant.WALL_HEIGHT + constant.WALL_HEIGHT
        pygame.draw.rect(
            self.screen,
            constant.WALL_COLOR,
            pygame.Rect(
                pos_x,
                pos_y,
                constant.WALL_HEIGHT,
                constant.WALL_WIDTH,
             ),
        )

    def draw_east(
        self,
        pos: tuple[int, int]
    ) -> None:
        pos_x: int = pos[0] * constant.WALL_WIDTH + constant.WALL_WIDTH
        pos_y: int = pos[1] * constant.WALL_HEIGHT
        pygame.draw.rect(
            self.screen,
            constant.WALL_COLOR,
            pygame.Rect(
                pos_x,
                pos_y,
                constant.WALL_WIDTH,
                constant.WALL_HEIGHT,
             ),
        )

    def draw_west(
        self,
        pos: tuple[int, int]
    ) -> None:
        pos_x: int = pos[0] * constant.WALL_WIDTH
        pos_y: int = pos[1] * constant.WALL_HEIGHT
        pygame.draw.rect(
            self.screen,
            constant.WALL_COLOR,
            pygame.Rect(
                pos_x,
                pos_y,
                constant.WALL_WIDTH,
                constant.WALL_HEIGHT,
             ),
        )
