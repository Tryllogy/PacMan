from mazegenerator import MazeGenerator
from .scenes import (
    GameState, Scene, MainScene,
    WinScene, LoseScene, PauseScene, InGameScene,
    HighscoreScene, InstructionsScene
)
from . import constant
import pygame
import sys
from .parsing.parser import Parser, Data
from pathlib import Path
from pydantic import ValidationError


def main() -> None:
    if len(sys.argv) == 1:
        print("Missing args")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Too many args")
        sys.exit(1)
    try:
        parser = Parser(Path(sys.argv[1]))
        config: Data = parser.get_data()
    except ValidationError as e:
        for error in e.errors():
            print(f'Value: {error["loc"][0]} -> {error["msg"]}')
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

    pygame.init()
    maze_gen: MazeGenerator = MazeGenerator((config.levels[0].width,
                                             config.levels[0].height))
    maze_gen.generate()
    screen = pygame.display.set_mode(
        (constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
    pygame.display.set_caption("PacMan")
    scenes: dict[str, Scene] = {
        GameState.MAIN.value: MainScene(screen),
        GameState.GAME.value: InGameScene(screen, maze_gen, config),
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
            sys.exit(0)

        next_scene = scenes[current_scene].handle_events(events)
        current_scene = next_scene

        scenes[current_scene].update()
        scenes[current_scene].draw()

        reset_all_scenes(scenes)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


def reset_all_scenes(
    scenes: dict[str, Scene]
) -> None:
    for k, scene in scenes.items():
        scene.current_scene = scene.base_scene


if __name__ == "__main__":
    # try:
    #     main()
    # except Exception as e:
    #     print(e)
    main()
