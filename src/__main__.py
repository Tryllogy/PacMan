from mazegenerator import MazeGenerator
from .scenes import (
    GameState, Scene, MainScene,
    WinScene, LoseScene, PauseScene, InGameScene,
    HighscoreScene, InstructionsScene
)
from . import constant
import pygame
import sys
from .entity import Score
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
    screen = pygame.display.set_mode(
        (constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
    pygame.display.set_caption("PacMan")
    score: Score = Score()

    def new_game_scene() -> InGameScene:
        maze_gen: MazeGenerator = MazeGenerator(
            (config.levels[0].width, config.levels[0].height),
            seed=config.seed)
        maze_gen.generate(config.seed)
        score.score = 0
        return InGameScene(screen, maze_gen, config, score)

    scenes: dict[str, Scene] = {
        GameState.MAIN.value: MainScene(screen),
        GameState.GAME.value: new_game_scene(),
        GameState.PAUSE.value: PauseScene(screen),
        GameState.WIN.value: WinScene(screen, config, score),
        GameState.LOSE.value: LoseScene(screen, config, score),
        GameState.HIGHSCORE.value: HighscoreScene(screen,
                                                  config.highscore_filename),
        GameState.INSTRUCTIONS.value: InstructionsScene(screen),
    }
    current_scene: str = GameState.MAIN.value
    pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()
    running = True
    while running:
        events = pygame.event.get()
        screen.fill((0, 0, 0))

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        prev_scene = current_scene
        next_scene = scenes[current_scene].handle_events(events)
        if (prev_scene == GameState.MAIN.value
                and next_scene == GameState.GAME.value):
            scenes[GameState.GAME.value] = new_game_scene()
        current_scene = next_scene

        next_scene = scenes[current_scene].update()
        current_scene = next_scene
        scenes[current_scene].draw()

        reset_all_scenes(scenes)
        pygame.display.flip()
        clock.tick(constant.FPS)

    pygame.quit()
    sys.exit(0)


def reset_all_scenes(
    scenes: dict[str, Scene]
) -> None:
    for k, scene in scenes.items():
        scene.current_scene = scene.base_scene


if __name__ == "__main__":
    main()
