from .scene import Scene, GameState
from .button import Button
from .. import constant


class InstructionsScene(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.current_scene = GameState.INSTRUCTIONS.value
        self.base_scene = self.current_scene
        x, y = self.middle_screen
        self.back_button: Button = Button(
            x,
            y,
            constant.BUTTON_WIDTH,
            constant.BUTTON_HEIGHT,
            "Back",
            self.back_main,
            self.font,
        )

    def back_main(
            self
    ) -> str:
        self.current_scene = GameState.MAIN.value
        return self.current_scene

    def handle_events(self, events):
        for event in events:
            self.back_button.handle_event(event)
        return self.current_scene

    def draw(
        self,
    ) -> None:
        self.back_button.draw(self.screen)
