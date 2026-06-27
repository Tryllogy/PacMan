from mazegenerator import MazeGenerator
from .scene import Scene, GameState
from ..phantom import Phantom
from ..player import Player
from ..wall import Wall
from .. import constant
from enum import Enum
import pygame


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
        self.maze_gen: MazeGenerator = maze_gen
        self.phantoms: list[Phantom] = []
        self.player: Player = None
        self.cheat_invicible: bool = False
        self.offset: tuple[int, int] = self.get_offset()
        self.walls: list[Wall] = []
        self.make_wall()

    def get_offset(
        self
    ) -> None:
        maze_size_px: tuple[int, int] = (
            len(self.maze_gen.maze) * constant.WALL_HEIGHT,
            len(self.maze_gen.maze[0]) * constant.WALL_HEIGHT)
        offset: tuple[int, int] = (
            self.middle_screen[0] - maze_size_px[0] / 2,
            self.middle_screen[1] - maze_size_px[1] / 2
        )
        return offset

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
        for wall in self.walls:
            wall.draw(self.screen)

    def make_wall(
        self
    ) -> None:
        for y, line in enumerate(self.maze_gen.maze):
            for x, value in enumerate(line):
                pos: tuple[int, int] = (x, y)
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
        pos_x: int = pos[0] * constant.WALL_HEIGHT
        pos_y: int = pos[1] * constant.WALL_HEIGHT
        self.walls.append(Wall(
            self.offset[0] + pos_x,
            self.offset[1] + pos_y,
            constant.WALL_HEIGHT,
            constant.WALL_WIDTH,
        ))

    def draw_south(
        self,
        pos: tuple[int, int]
    ) -> None:
        offset: int = constant.WALL_HEIGHT
        pos_x: int = pos[0] * constant.WALL_HEIGHT
        pos_y: int = pos[1] * constant.WALL_HEIGHT + offset
        self.walls.append(Wall(
            self.offset[0] + pos_x,
            self.offset[1] + pos_y,
            constant.WALL_HEIGHT,
            constant.WALL_WIDTH,
        ))

    def draw_east(
        self,
        pos: tuple[int, int]
    ) -> None:
        offset: int = constant.WALL_HEIGHT
        pos_x: int = pos[0] * constant.WALL_HEIGHT + offset
        pos_y: int = pos[1] * constant.WALL_HEIGHT
        self.walls.append(Wall(
            self.offset[0] + pos_x,
            self.offset[1] + pos_y,
            constant.WALL_WIDTH,
            constant.WALL_HEIGHT + constant.WALL_WIDTH,
        ))

    def draw_west(
        self,
        pos: tuple[int, int]
    ) -> None:
        pos_x: int = pos[0] * constant.WALL_HEIGHT
        pos_y: int = pos[1] * constant.WALL_HEIGHT
        self.walls.append(Wall(
            self.offset[0] + pos_x,
            self.offset[1] + pos_y,
            constant.WALL_WIDTH,
            constant.WALL_HEIGHT,
        ))
