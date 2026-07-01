from mazegenerator import MazeGenerator
from .scene import Scene, GameState
from ..strategies import AggressiveStrategy
from ..entity import (Phantom, Player, Direction,
                      Wall, Pacgum, SuperPacgum)
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
        maze_gen: MazeGenerator,
        points_per_pacgum: int = 1,
        points_per_superpacgum: int = 5,
        points_per_ghost: int = 10
    ) -> None:
        super().__init__(screen)
        self.points_per_pacgum: int = points_per_pacgum
        self.points_per_superpacgum: int = points_per_superpacgum
        self.points_per_ghost: int = points_per_ghost
        self.current_scene = GameState.GAME.value
        self.base_scene = self.current_scene
        self.maze_gen: MazeGenerator = maze_gen
        self.phantoms: list[Phantom] = []
        self.player: Player = None
        self.offset: tuple[int, int] = self.get_offset()
        self.walls: list[Wall] = []
        self.pacgums: list[Pacgum] = []
        self.super_pacgums: list[SuperPacgum] = []
        self.make_wall()
        self.make_pacgum()
        self.make_phantom()
        self.make_player()

    def update(
        self
    ) -> None:

        for phantom in self.phantoms:
            #  have to move this block 
            #  Start
            maze_case_h = len(self.maze_gen.maze)
            maze_case_w = len(self.maze_gen.maze[0])
            screen_pxl_w, screen_pxl_h = self.screen.get_size()
            maze_pxl_h, maze_pxl_w = self.maze_size_px
            offset_w = (screen_pxl_w - maze_pxl_w) / 2
            offset_h = (screen_pxl_h - maze_pxl_h) / 2
            ppc_x = maze_pxl_w / maze_case_w
            ppc_y = maze_pxl_h / maze_case_h
            print('ppc, x, y', ppc_x, ppc_y)
            print("maze size pxl", self.maze_size_px)
            print('screen size pxl', screen_pxl_w, screen_pxl_h)
            print("player pxl", self.player.x, self.player.y)
            print("offset", offset_w, offset_h)
            print(maze_case_w, maze_case_h)
            player_maze_y = int((self.player.y - offset_h) // ppc_y)  # maze_case_h
            player_maze_x = int((self.player.x - offset_w) // ppc_x)  # maze_case_w
            print(player_maze_x, player_maze_y)
            player_pos = (player_maze_x, player_maze_y)
            #  End
            phantom.update(player_pos)
            phantom.move()
        self.player.update(self.walls, self.pacgums, self.super_pacgums)

    def handle_events(
        self,
        events
    ) -> str:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                print("PAUSE")
                self.current_scene = GameState.PAUSE.value
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.player.next_direction = Direction.UP
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.player.next_direction = Direction.DOWN
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.player.next_direction = Direction.LEFT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.player.next_direction = Direction.RIGHT
        return self.current_scene

    def draw(
        self,
    ) -> None:
        super().draw()
        for wall in self.walls:
            wall.draw(self.screen)
        for pacgum in self.pacgums:
            pacgum.draw(self.screen)
        for super_pacgum in self.super_pacgums:
            super_pacgum.draw(self.screen)
        for phantom in self.phantoms:
            phantom.draw(self.screen)
        self.player.draw(self.screen)

    def get_offset(
        self
    ) -> None:
        self.maze_size_px: tuple[int, int] = (
            len(self.maze_gen.maze) * constant.WALL_HEIGHT,
            len(self.maze_gen.maze[0]) * constant.WALL_HEIGHT)
        offset: tuple[int, int] = (
            self.middle_screen[0] - self.maze_size_px[0] / 2,
            self.middle_screen[1] - self.maze_size_px[1] / 2
        )
        return offset

    def find_open_middle_maze(
        self
    ) -> tuple[int, int]:
        middle_maze_x: int = len(self.maze_gen.maze) // 2 - 1
        middle_maze_y: int = len(self.maze_gen.maze[0]) // 2 - 1
        while self.maze_gen.maze[middle_maze_x][middle_maze_y] == 15:
            middle_maze_x += 1
            if middle_maze_x >= len(self.maze_gen.maze):
                middle_maze_x = 0
                middle_maze_y += 1
                if middle_maze_y >= len(self.maze_gen.maze[0]):
                    raise ValueError("No open space in the maze")
        return (middle_maze_x, middle_maze_y)

    def make_player(
        self
    ) -> None:
        middle_maze_x, middle_maze_y = self.find_open_middle_maze()
        offset_player: int = constant.WALL_WIDTH * 1.3

        pox_x: int = middle_maze_x * constant.WALL_HEIGHT
        pox_y: int = middle_maze_y * constant.WALL_HEIGHT
        self.player = Player(
            self.offset[0] + offset_player + pox_x,
            self.offset[1] + offset_player + pox_y,
            self.offset[0] + offset_player,
            self.offset[1] + offset_player,
            points_per_pacgum=self.points_per_pacgum,
            points_per_superpacgum=self.points_per_superpacgum,
            points_per_ghost=self.points_per_ghost
        )

    def make_pacgum(
        self
    ) -> None:
        offset_pacgum: int = constant.WALL_HEIGHT / 2 + constant.WALL_WIDTH / 2
        for y, line in enumerate(self.maze_gen.maze):
            for x, value in enumerate(line):
                if value == 15:
                    continue

                pos_x: int = x * constant.WALL_HEIGHT
                pos_y: int = y * constant.WALL_HEIGHT
                if self.is_corner(x, y):
                    self.super_pacgums.append(SuperPacgum(
                        pos_x + self.offset[0] + offset_pacgum,
                        pos_y + self.offset[1] + offset_pacgum
                    ))
                else:
                    self.pacgums.append(Pacgum(
                        pos_x + self.offset[0] + offset_pacgum,
                        pos_y + self.offset[1] + offset_pacgum
                    ))

    def make_phantom(self):
        offset_phantom: int = constant.WALL_WIDTH * 1.3
        mx, my = self.maze_size_px
        mx -= constant.WALL_HEIGHT
        my -= constant.WALL_HEIGHT
        y = len(self.maze_gen.maze) - 1
        x = len(self.maze_gen.maze[0]) - 1
        maze_case_h = len(self.maze_gen.maze)
        maze_case_w = len(self.maze_gen.maze[0])
        screen_pxl_w, screen_pxl_h = self.screen.get_size()
        maze_pxl_h, maze_pxl_w = self.maze_size_px
        offset_w = (screen_pxl_w - maze_pxl_w) / 2
        offset_h = (screen_pxl_h - maze_pxl_h) / 2
        ppc_x = maze_pxl_w / maze_case_w
        ppc_y = maze_pxl_h / maze_case_h
        print('ppc, x, y', ppc_x, ppc_y)
        print("maze size pxl", self.maze_size_px)
        print('screen size pxl', screen_pxl_w, screen_pxl_h)
        print("offset", offset_w, offset_h)
        print(maze_case_w, maze_case_h)
        self.phantoms.append(Phantom(
            0 + self.offset[0] + offset_phantom,
            0 + self.offset[1] + offset_phantom,
            AggressiveStrategy(self.maze_gen.maze),
            "purple",
            (x, y),
            (ppc_x, ppc_y),
            (offset_w, offset_h)
        ))
        self.phantoms.append(Phantom(
            mx + self.offset[0] + offset_phantom,
            0 + self.offset[1] + offset_phantom,
            AggressiveStrategy(self.maze_gen.maze),
            "green",
            (0, 0),
            (ppc_x, ppc_y),
            (offset_w, offset_h)
        ))
        self.phantoms.append(Phantom(
            0 + self.offset[0] + offset_phantom,
            my + self.offset[1] + offset_phantom,
            AggressiveStrategy(self.maze_gen.maze),
            "blue",
            (x, 0),
            (ppc_x, ppc_y),
            (offset_w, offset_h)
        ))
        self.phantoms.append(Phantom(
            my + self.offset[0] + offset_phantom,
            mx + self.offset[1] + offset_phantom,
            AggressiveStrategy(self.maze_gen.maze),
            "red",
            (0, y),
            (ppc_x, ppc_y),
            (offset_w, offset_h)
        ))

    def make_wall(
        self
    ) -> None:
        for y, line in enumerate(self.maze_gen.maze):
            for x, value in enumerate(line):
                pos: tuple[int, int] = (x, y)
                if value >> 3 & 1:
                    self.make_wall_west(pos)
                if value >> 2 & 1:
                    self.make_wall_south(pos)
                if value >> 1 & 1:
                    self.make_wall_east(pos)
                if value & 1:
                    self.make_wall_north(pos)

    def make_wall_north(
        self,
        pos: tuple[int, int],
    ) -> None:
        pos_x: int = pos[0] * constant.WALL_HEIGHT
        pos_y: int = pos[1] * constant.WALL_HEIGHT
        self.walls.append(Wall(
            self.offset[0] + pos_x,
            self.offset[1] + pos_y,
            constant.WALL_HEIGHT + constant.WALL_WIDTH,
            constant.WALL_WIDTH,
        ))

    def make_wall_south(
        self,
        pos: tuple[int, int]
    ) -> None:
        offset: int = constant.WALL_HEIGHT
        pos_x: int = pos[0] * constant.WALL_HEIGHT
        pos_y: int = pos[1] * constant.WALL_HEIGHT + offset
        self.walls.append(Wall(
            self.offset[0] + pos_x,
            self.offset[1] + pos_y,
            constant.WALL_HEIGHT + constant.WALL_WIDTH,
            constant.WALL_WIDTH,
        ))

    def make_wall_east(
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

    def make_wall_west(
        self,
        pos: tuple[int, int]
    ) -> None:
        pos_x: int = pos[0] * constant.WALL_HEIGHT
        pos_y: int = pos[1] * constant.WALL_HEIGHT
        self.walls.append(Wall(
            self.offset[0] + pos_x,
            self.offset[1] + pos_y,
            constant.WALL_WIDTH,
            constant.WALL_HEIGHT + constant.WALL_WIDTH,
        ))

    def is_corner(
        self,
        x: int,
        y: int
    ) -> bool:
        if y == 0 and x == 0:
            return True
        if y == len(self.maze_gen.maze[0]) - 1 and x == 0:
            return True
        if y == 0 and x == len(self.maze_gen.maze) - 1:
            return True
        if (y == len(self.maze_gen.maze[0]) - 1 and
                x == len(self.maze_gen.maze) - 1):
            return True
        return False
