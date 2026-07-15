from typing import TYPE_CHECKING
from .color import Color
if TYPE_CHECKING:
    from .surface import Rect
CHAR_WIDTH = 10
CHAR_HEIGHT = 20


class Text:
    """A rendered string: just its text and colour, drawn later as overlay."""

    def __init__(self, text: str, color: Color) -> None:
        self.text: str = text
        self.color: Color = color
        self.width: int = len(text) * CHAR_WIDTH
        self.height: int = CHAR_HEIGHT

    def get_size(self) -> tuple[int, int]:
        return (self.width, self.height)

    def get_rect(
        self,
        center: tuple[int, int] | None = None,
        topleft: tuple[int, int] | None = None,
    ) -> "Rect":
        from .surface import Rect
        rect = Rect(0, 0, self.width, self.height)
        if center is not None:
            rect.x = center[0] - self.width // 2
            rect.y = center[1] - self.height // 2
        elif topleft is not None:
            rect.x, rect.y = topleft
        return rect


class Font:
    """Drop-in stand-in for ``pygame.font.Font`` backed by the MLX font."""

    def __init__(self, name: str | None = None, size: int = 40) -> None:
        self.size: int = size

    def render(
        self,
        text: str,
        antialias: bool = True,
        color: Color = (255, 255, 255),
    ) -> Text:
        return Text(text, color)
