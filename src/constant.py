import os
import sys


def _project_root() -> str:
    """Return the root of the project, which is the parent of
    the directory containing this file.
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _bundle_dir() -> str:
    """Return the directory containing the bundled executable,
    or the project root if not bundled."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return str(sys._MEIPASS)
    return _project_root()


def _data_dir() -> str:
    """Return the directory containing the data files, which is the project
    root if not bundled, or the parent of the executable if bundled."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return _project_root()


_BUNDLE_DIR = _bundle_dir()
_DATA_DIR = _data_dir()

TEXT_COLOR_BASE = (171, 173, 21)

BUTTON_COLOR_BASE = (14, 24, 138)
BUTTON_COLOR_HOVER = (16, 32, 222)

WALL_COLOR = (14, 24, 138)
WALL_WIDTH = 10
WALL_HEIGHT = 40

PACGUM_COLOR = (255, 255, 255)
PACGUM_SIZE = 8
SUPERPACGUM_COLOR = (255, 255, 255)
SUPERPACGUM_SIZE = 16

BUTTON_WIDTH = 250
BUTTON_HEIGHT = 100

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

PLAYER_SPEED = 2
PLAYER_SPRITE_CHANGE_DELAY = 150
GHOST_SPRITE_CHANGE_DELAY = 500

RETREAT_TIME = 8
RESPAWN_TIME = 10

FPS = 60
SCORE_DIR = os.path.join(_DATA_DIR, "src", "score")
SPRITE_DIR = os.path.join(_BUNDLE_DIR, "src", "sprites")

MAX_HIGHSCORES = 10
MAX_NAME_LENGTH = 10
