from mazegenerator import MazeGenerator
from src.scenes import (
    GameState, Scene, MainScene,
    WinScene, LoseScene, PauseScene, InGameScene,
    HighscoreScene, InstructionsScene
)
from src import constant
from src.graphics import app, Event
import sys
from src.entity import Score
from src.parsing.parser import Parser, Data
from pathlib import Path


def main() -> None:
    if len(sys.argv) == 1:
        print("Missing args")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Too many args")
        sys.exit(1)
    if not sys.argv[1].endswith(".json"):
        print("Config file must be a .json file")
        sys.exit(1)
    try:
        parser = Parser(Path(sys.argv[1]))
        config: Data = parser.get_data()
    except FileNotFoundError:
        print(f"Config file not found: {sys.argv[1]}")
        sys.exit(1)
    except Exception as e:
        print(f"Invalid config file: {e}")
        sys.exit(1)

    app.init(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, "PacMan",
             fps=constant.FPS)
    screen = app.screen
    assert screen is not None
    score: Score = Score()

    def new_game_scene() -> InGameScene:
        maze_gen: MazeGenerator = MazeGenerator(
            (config.levels[0].width, config.levels[0].height),
            perfect=False,
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
    current_scene = GameState.MAIN.value
    rendered_scene: str | None = None

    def frame(events: list[Event]) -> None:
        nonlocal current_scene, rendered_scene
        prev_scene = current_scene
        next_scene = scenes[current_scene].handle_events(events)
        if (prev_scene == GameState.MAIN.value
                and next_scene == GameState.GAME.value):
            scenes[GameState.GAME.value] = new_game_scene()
        current_scene = next_scene

        next_scene = scenes[current_scene].update()
        current_scene = next_scene

        scene = scenes[current_scene]
        if (current_scene == GameState.GAME.value
                or current_scene != rendered_scene
                or scene.dirty):
            scene.draw()
            scene.dirty = False
            rendered_scene = current_scene
            app.mark_dirty()

        reset_all_scenes(scenes)

    app.run(frame)
    sys.exit(0)


def reset_all_scenes(
    scenes: dict[str, Scene]
) -> None:
    for k, scene in scenes.items():
        scene.current_scene = scene.base_scene


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
