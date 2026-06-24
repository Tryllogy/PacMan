from mazegenerator import MazeGenerator
from .scenes import (
    GameState, Scene, MainScene,
    WinScene, LoseScene, PauseScene, InGameScene,
    HighscoreScene, InstructionsScene
)
from . import constant
import pygame
import sys


def main():
    pygame.init()
    config = {
        "size": (15, 15),
    }
    maze_gen: MazeGenerator = MazeGenerator(**config)
    maze_gen.generate()
    screen = pygame.display.set_mode(
        (constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
    scenes: dict[str, Scene] = {
        GameState.MAIN.value: MainScene(screen),
        GameState.GAME.value: InGameScene(screen),
        GameState.PAUSE.value: PauseScene(screen),
        GameState.WIN.value: WinScene(screen),
        GameState.LOSE.value: LoseScene(screen),
        GameState.HIGHSCORE.value: HighscoreScene(screen),
        GameState.INSTRUCTIONS.value: InstructionsScene(screen),
    }
    current_scene: str = GameState.MAIN.value

    pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        screen.fill((0, 0, 0))

        if any(event.type == pygame.QUIT or
               (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
               for event in events):
            pygame.quit()
            sys.exit()

        next_scene = scenes[current_scene].handle_events(events)
        current_scene = next_scene

        scenes[current_scene].update()
        scenes[current_scene].draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
