from .scene import Scene, GameState
from ..button import Button
from .. import constant


PLAY_X = -150
PLAY_Y = -100
HIGHSCORE_X = -150
HIGHSCORE_Y = -50
INSTRUCTIONS_X = -150
INSTRUCTIONS_Y = 0
EXIT_X = -150
EXIT_Y = 50


class MainScene(Scene):
    def __init__(
        self,
        screen
    ) -> None:
        super().__init__(screen)
        mx, my = self.middle_screen

        self.play_button: Button = Button(
            mx - PLAY_X,
            my - PLAY_Y,
            constant.BUTTON_WIDTH,
            constant.BUTTON_HEIGHT,
            "Play",
            self.start_game,
            self.font
        )

        self.high_score_button: Button = Button(
            mx - HIGHSCORE_X,
            my - HIGHSCORE_Y,
            constant.BUTTON_WIDTH,
            constant.BUTTON_HEIGHT,
            "View highscore",
            self.view_highscore,
            self.font
        )

    def view_highscore(
        self
    ) -> None:
        global current_scene
        current_scene = GameState.HIGHSCORE

    def start_game(
        self,
    ) -> None:
        global current_scene
        current_scene = GameState.GAME

    def handle_events(
        self,
        events
    ) -> GameState:
        for event in events:
            self.play_button.handle_event(event)
        return current_scene

    def draw(
        self,
        mouse_pos: tuple[int, int]
    ) -> None:
        super().draw(mouse_pos)
        self.play_button.draw(self.screen)
