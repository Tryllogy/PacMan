from .scene import Scene, GameState
from .button import Button
from .. import constant


PLAY_X = -150
PLAY_Y = -(constant.BUTTON_HEIGHT + 200)
HIGHSCORE_X = -150
HIGHSCORE_Y = -(constant.BUTTON_HEIGHT)
INSTRUCTIONS_X = -150
INSTRUCTIONS_Y = 100
EXIT_X = -150
EXIT_Y = (constant.BUTTON_HEIGHT + 200)


class MainScene(Scene):
    def __init__(
        self,
        screen
    ) -> None:
        super().__init__(screen)
        self.current_scene = GameState.MAIN.value
        self.base_scene = self.current_scene
        mx, my = self.middle_screen

        self.play_button: Button = Button(
            mx + PLAY_X,
            my + PLAY_Y,
            constant.BUTTON_WIDTH,
            constant.BUTTON_HEIGHT,
            "Play",
            self.start_game,
            self.font
        )

        self.high_score_button: Button = Button(
            mx + HIGHSCORE_X,
            my + HIGHSCORE_Y,
            constant.BUTTON_WIDTH,
            constant.BUTTON_HEIGHT,
            "View highscore",
            self.view_highscore,
            self.font
        )

        self.instructions_button: Button = Button(
            mx + INSTRUCTIONS_X,
            my + INSTRUCTIONS_Y,
            constant.BUTTON_WIDTH,
            constant.BUTTON_HEIGHT,
            "Instructions",
            self.view_instructions,
            self.font
        )

        self.exit_button: Button = Button(
            mx + EXIT_X,
            my + EXIT_Y,
            constant.BUTTON_WIDTH,
            constant.BUTTON_HEIGHT,
            "Exit",
            self.exit_program,
            self.font
        )

    def exit_program(self):
        import pygame
        import sys
        pygame.quit()
        sys.exit(0)

    def view_instructions(
        self
    ) -> str:
        self.current_scene = GameState.INSTRUCTIONS.value
        return self.current_scene

    def view_highscore(
        self
    ) -> str:
        self.current_scene = GameState.HIGHSCORE.value
        return self.current_scene

    def start_game(
        self,
    ) -> str:
        self.current_scene = GameState.GAME.value
        return self.current_scene

    def handle_events(
        self,
        events
    ) -> str:
        for event in events:
            self.play_button.handle_event(event)
            self.high_score_button.handle_event(event)
            self.instructions_button.handle_event(event)
            self.exit_button.handle_event(event)
        return self.current_scene

    def draw(
        self,
    ) -> None:
        super().draw()
        self.play_button.draw(self.screen)
        self.high_score_button.draw(self.screen)
        self.instructions_button.draw(self.screen)
        self.exit_button.draw(self.screen)
