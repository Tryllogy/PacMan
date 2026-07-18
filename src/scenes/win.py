from .end_scene import EndScene
from .scene import GameState
from ..parsing import Data
from ..entity import Score
from ..graphics import Surface


class WinScene(EndScene):
    def __init__(
        self,
        screen: Surface,
        config: Data,
        score: Score
    ) -> None:
        super().__init__(
            screen, config, score,
            GameState.WIN, "You Win!", (0, 255, 0),
            subtitle="Congratulations, you cleared every level!")
