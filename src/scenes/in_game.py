from mazegenerator import MazeGenerator
from ..utils.converter import Converter
from ..parsing import Data
from .scene import Scene, GameState
from ..strategies import (AggressiveStrategy, RandomStrategy, ZoneStrategy)
from ..entity import (Phantom, Player, Direction,
                      Wall, Pacgum, SuperPacgum, Score)
from ..graphics import Event, EventType, Surface
from ..graphics import events as ev
from .. import constant
from enum import Enum
import math


class Walls(Enum):
    N = 1
    E = 2
    S = 4
    W = 8


class InGameScene(Scene):
    def __init__(
        self,
        screen: Surface,
        maze_gen: MazeGenerator,
        config: Data,
        score: Score
    ) -> None:
        super().__init__(screen)
        self.config: Data = config
        self.points_per_pacgum: int = config.points_per_pacgum
        self.points_per_super_pacgum: int = config.points_per_super_pacgum
        self.points_per_ghost: int = config.points_per_ghost
        self.level_max_time: int = config.level_max_time
        self.timer: int = self.level_max_time
        self.current_scene = GameState.GAME.value
        self.base_scene = self.current_scene
        self.maze_gen: MazeGenerator = maze_gen
        self.level_index: int = 0
        self.phantoms: list[Phantom] = []
        self.player: Player
        self.maze_origin: tuple[int, int] = self.get_offset()
        self.walls: list[Wall] = []
        self.pacgums: list[Pacgum] = []
        self.super_pacgums: list[SuperPacgum] = []
        self.score: Score = score
        self.init_converter()
        self.make_wall()
        self.make_pacgum()
        self.make_phantom()
        self.make_player(self.config.lives)

    def update(
        self
    ) -> str:
        for phantom in self.phantoms:
            player_cell = self.converter.pixel_to_cell(
                (self.player.pixel_x, self.player.pixel_y))
            phantom.update(player_cell)

        self.player.update(self.walls, self.pacgums, self.super_pacgums,
                           self.phantoms)

        if self.player.lives <= 0:
            self.current_scene = GameState.LOSE.value
        if len(self.pacgums) == 0 and len(self.super_pacgums) == 0:
            self.new_level()
        return self.current_scene

    def init_converter(self) -> None:
        maze_rows = len(self.maze_gen.maze)
        maze_cols = len(self.maze_gen.maze[0])
        self.converter = Converter(
            (maze_rows, maze_cols),
            self.maze_size_px,
            self.screen.get_size())

    def new_level(
        self
    ) -> None:
        self.level_index += 1
        if self.level_index >= len(self.config.levels):
            self.current_scene = GameState.WIN.value
        else:
            self.timer = self.level_max_time
            self.phantoms.clear()
            self.walls.clear()
            self.pacgums.clear()
            self.super_pacgums.clear()
            self.generate_maze()
            self.maze_origin = self.get_offset()
            self.init_converter()
            self.make_wall()
            self.make_pacgum()
            self.make_phantom()
            self.make_player(self.player.lives)

    def handle_events(
        self,
        events: list[Event]
    ) -> str:
        for event in events:
            if (event.type == EventType.TIMER
                    and event.timer_id == ev.TIMER_GAME):
                if self.timer > 0:
                    self.timer -= 1
                    if self.timer <= 0:
                        self.current_scene = GameState.LOSE.value
            if event.type == EventType.KEYDOWN and event.key == ev.K_i:
                self.player.invincible = not self.player.invincible
            if event.type == EventType.KEYDOWN and event.key == ev.K_p:
                self.new_level()
            if event.type == EventType.KEYDOWN and event.key == ev.K_ESCAPE:
                self.current_scene = GameState.PAUSE.value
            if event.type == EventType.KEYDOWN and event.key in (
                    ev.K_UP, ev.K_w):
                self.player.next_direction = Direction.UP
            if event.type == EventType.KEYDOWN and event.key in (
                    ev.K_DOWN, ev.K_s):
                self.player.next_direction = Direction.DOWN
            if event.type == EventType.KEYDOWN and event.key in (
                    ev.K_LEFT, ev.K_a):
                self.player.next_direction = Direction.LEFT
            if event.type == EventType.KEYDOWN and event.key in (
                    ev.K_RIGHT, ev.K_d):
                self.player.next_direction = Direction.RIGHT
            if (event.type == EventType.TIMER
                    and event.timer_id == ev.TIMER_GHOST):
                for phantom in self.phantoms:
                    if phantom.retreat:
                        if phantom.retreat_timer > 0:
                            phantom.retreat_timer -= 1
                            if phantom.retreat_timer <= 0:
                                phantom.reset_strategy()
                    if phantom.to_spawn:
                        if phantom.respawn_timer > 0:
                            phantom.respawn_timer -= 1
                            if phantom.respawn_timer <= 0:
                                phantom.reset_strategy()
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
        self.draw_score()
        self.draw_lives()
        self.draw_level()
        self.draw_timer()
        self.draw_cheat()

    def generate_maze(
        self
    ) -> None:
        self.maze_gen = MazeGenerator(
            (self.config.levels[self.level_index].width,
                self.config.levels[self.level_index].height),
            perfect=False)
        self.maze_gen.generate()

    def draw_timer(
        self,
    ) -> None:
        timer_text = self.font.render(f"Time: {self.timer}",
                                      True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 130))

    def draw_cheat(
        self,
    ) -> None:
        if self.player.invincible:
            state, color = "ON", (0, 255, 0)
        else:
            state, color = "OFF", (128, 128, 128)
        cheat_text = self.font.render(f"Cheat: {state}", True, color)
        self.screen.blit(cheat_text, (10, 170))

    def draw_score(
        self
    ) -> None:
        score_text = self.font.render(f"Score: {self.score.score}",
                                      True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_lives(
        self
    ) -> None:
        lives_text = self.font.render(f"Lives: {self.player.lives}",
                                      True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 50))

    def draw_level(
        self
    ) -> None:
        level_text = self.font.render(
            f"{self.config.levels[self.level_index].name}",
            True, (255, 255, 255))
        self.screen.blit(level_text, (10, 90))

    def get_offset(
        self
    ) -> tuple[int, int]:
        maze_height_px = len(self.maze_gen.maze) * constant.WALL_HEIGHT
        maze_width_px = len(self.maze_gen.maze[0]) * constant.WALL_HEIGHT
        self.maze_size_px: tuple[int, int] = (maze_height_px, maze_width_px)
        maze_origin: tuple[int, int] = (
            int(self.middle_screen[0] - maze_width_px / 2),
            int(self.middle_screen[1] - maze_height_px / 2)
        )
        return maze_origin

    def find_open_middle_maze(
        self
    ) -> tuple[int, int]:
        middle_row: int = math.ceil(len(self.maze_gen.maze) / 2) - 1
        middle_col: int = math.ceil(len(self.maze_gen.maze[0]) / 2) - 1
        while self.maze_gen.maze[middle_row][middle_col] == 15:
            middle_row += 1
            if middle_row >= len(self.maze_gen.maze):
                middle_row = 0
                middle_col += 1
                if middle_col >= len(self.maze_gen.maze[0]):
                    raise ValueError("No open space in the maze")
        return (middle_row, middle_col)

    def make_player(
        self,
        lives: int,
    ) -> None:
        middle_row, middle_col = self.find_open_middle_maze()
        offset_player: int = int(constant.WALL_WIDTH * 1.3)

        pixel_x: int = middle_col * constant.WALL_HEIGHT
        pixel_y: int = middle_row * constant.WALL_HEIGHT
        self.player = Player(
            self.maze_origin[0] + offset_player + pixel_x,
            self.maze_origin[1] + offset_player + pixel_y,
            self.maze_origin[0] + offset_player,
            self.maze_origin[1] + offset_player,
            self.score,
            lives,
            self.config.points_per_pacgum,
            self.config.points_per_super_pacgum,
            self.config.points_per_ghost,
        )

    def make_pacgum(
        self
    ) -> None:
        middle_row, middle_col = self.find_open_middle_maze()
        offset_pacgum: int = int(
            constant.WALL_HEIGHT / 2 + constant.WALL_WIDTH / 2)
        for row, line in enumerate(self.maze_gen.maze):
            for col, value in enumerate(line):
                if value == 15 or (row == middle_row and col == middle_col):
                    continue

                pixel_x: int = col * constant.WALL_HEIGHT
                pixel_y: int = row * constant.WALL_HEIGHT
                if self.is_corner(row, col):
                    self.super_pacgums.append(SuperPacgum(
                        pixel_x + self.maze_origin[0] + offset_pacgum,
                        pixel_y + self.maze_origin[1] + offset_pacgum
                    ))
                else:
                    self.pacgums.append(Pacgum(
                        pixel_x + self.maze_origin[0] + offset_pacgum,
                        pixel_y + self.maze_origin[1] + offset_pacgum
                    ))

    def make_phantom(self) -> None:
        offset_phantom: int = int(constant.WALL_WIDTH * 1.3)
        maze_height_px, maze_width_px = self.maze_size_px
        maze_height_px -= constant.WALL_HEIGHT
        maze_width_px -= constant.WALL_HEIGHT
        last_row = len(self.maze_gen.maze) - 1
        last_col = len(self.maze_gen.maze[0]) - 1
        self.phantoms.append(Phantom(
            0 + self.maze_origin[0] + offset_phantom,
            0 + self.maze_origin[1] + offset_phantom,
            AggressiveStrategy(self.maze_gen.maze),
            "purple",
            (0, 0),
            self.converter
        ))
        self.phantoms.append(Phantom(
            maze_width_px + self.maze_origin[0] + offset_phantom,
            0 + self.maze_origin[1] + offset_phantom,
            AggressiveStrategy(self.maze_gen.maze),
            "green",
            (0, last_col),
            self.converter
        ))
        self.phantoms.append(Phantom(
            0 + self.maze_origin[0] + offset_phantom,
            maze_height_px + self.maze_origin[1] + offset_phantom,
            RandomStrategy(self.maze_gen.maze, (last_row, 0)),
            "blue",
            (last_row, 0),
            self.converter
        ))
        self.phantoms.append(Phantom(
            maze_width_px + self.maze_origin[0] + offset_phantom,
            maze_height_px + self.maze_origin[1] + offset_phantom,
            ZoneStrategy(self.maze_gen.maze),
            "red",
            (last_row, last_col),
            self.converter
        ))

    def make_wall(
        self
    ) -> None:
        for row, line in enumerate(self.maze_gen.maze):
            for col, value in enumerate(line):
                cell: tuple[int, int] = (row, col)
                if value >> 3 & 1:
                    self.make_wall_west(cell)
                if value >> 2 & 1:
                    self.make_wall_south(cell)
                if value >> 1 & 1:
                    self.make_wall_east(cell)
                if value & 1:
                    self.make_wall_north(cell)

    def make_wall_north(
        self,
        cell: tuple[int, int],
    ) -> None:
        pixel_x: int = cell[1] * constant.WALL_HEIGHT
        pixel_y: int = cell[0] * constant.WALL_HEIGHT
        self.walls.append(Wall(
            self.maze_origin[0] + pixel_x,
            self.maze_origin[1] + pixel_y,
            constant.WALL_HEIGHT + constant.WALL_WIDTH,
            constant.WALL_WIDTH,
        ))

    def make_wall_south(
        self,
        cell: tuple[int, int]
    ) -> None:
        offset: int = constant.WALL_HEIGHT
        pixel_x: int = cell[1] * constant.WALL_HEIGHT
        pixel_y: int = cell[0] * constant.WALL_HEIGHT + offset
        self.walls.append(Wall(
            self.maze_origin[0] + pixel_x,
            self.maze_origin[1] + pixel_y,
            constant.WALL_HEIGHT + constant.WALL_WIDTH,
            constant.WALL_WIDTH,
        ))

    def make_wall_east(
        self,
        cell: tuple[int, int]
    ) -> None:
        offset: int = constant.WALL_HEIGHT
        pixel_x: int = cell[1] * constant.WALL_HEIGHT + offset
        pixel_y: int = cell[0] * constant.WALL_HEIGHT
        self.walls.append(Wall(
            self.maze_origin[0] + pixel_x,
            self.maze_origin[1] + pixel_y,
            constant.WALL_WIDTH,
            constant.WALL_HEIGHT + constant.WALL_WIDTH,
        ))

    def make_wall_west(
        self,
        cell: tuple[int, int]
    ) -> None:
        pixel_x: int = cell[1] * constant.WALL_HEIGHT
        pixel_y: int = cell[0] * constant.WALL_HEIGHT
        self.walls.append(Wall(
            self.maze_origin[0] + pixel_x,
            self.maze_origin[1] + pixel_y,
            constant.WALL_WIDTH,
            constant.WALL_HEIGHT + constant.WALL_WIDTH,
        ))

    def is_corner(
        self,
        row: int,
        col: int
    ) -> bool:
        last_row = len(self.maze_gen.maze) - 1
        last_col = len(self.maze_gen.maze[0]) - 1
        if row == 0 and col == 0:
            return True
        if row == last_row and col == 0:
            return True
        if row == 0 and col == last_col:
            return True
        if row == last_row and col == last_col:
            return True
        return False
