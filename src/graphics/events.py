from enum import Enum


class EventType(Enum):
    KEYDOWN = "keydown"
    QUIT = "quit"
    TIMER = "timer"


K_ESCAPE = 0xFF1B
K_RETURN = 0xFF0D
K_KP_ENTER = 0xFF8D
K_BACKSPACE = 0xFF08
K_UP = 0xFF52
K_DOWN = 0xFF54
K_LEFT = 0xFF51
K_RIGHT = 0xFF53

K_w = ord("w")
K_a = ord("a")
K_s = ord("s")
K_d = ord("d")
K_i = ord("i")
K_p = ord("p")
K_m = ord("m")
K_q = ord("q")
K_1 = ord("1")
K_2 = ord("2")
K_3 = ord("3")

TIMER_GAME = 1
TIMER_GHOST = 2


class Event:
    """A minimal event carrying a keysym or a timer id."""

    def __init__(
        self,
        type: EventType,
        key: int = 0,
        char: str = "",
        timer_id: int = 0,
    ) -> None:
        self.type: EventType = type
        self.key: int = key
        self.char: str = char
        self.timer_id: int = timer_id


def keysym_to_char(keysym: int) -> str:
    """Return the printable character for a keysym, or '' if none."""
    if 32 <= keysym <= 126:
        return chr(keysym)
    return ""
