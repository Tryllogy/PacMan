from __future__ import annotations
import time
from typing import Callable
from mlx import Mlx
from .events import (Event, EventType, TIMER_GAME, TIMER_GHOST,
                     keysym_to_char)
from .surface import Surface

_KEY_PRESS_EVENT = 2
_KEY_PRESS_MASK = 1
_DESTROY_NOTIFY = 33
_PRESENT_REPEAT = 4


def get_ticks() -> int:
    """Milliseconds since an arbitrary epoch (monotonic)."""
    return int(time.monotonic() * 1000)


class MlxApp:
    """Owns the MLX context, the screen surface and the frame loop."""

    def __init__(self) -> None:
        self.mlx: Mlx | None = None
        self.mlx_ptr = None
        self.win = None
        self.screen: Surface | None = None
        self._img = None
        self._width: int = 0
        self._height: int = 0
        self._events: list[Event] = []
        self._frame_cb: Callable[[list[Event]], None] | None = None
        self._should_exit: bool = False
        self._fps: int = 60
        self._last_frame: float = 0.0
        self._second_accum: float = 0.0
        self._present_frames: int = 0

    def init(self, width: int, height: int, title: str, fps: int = 60) -> None:
        self._width = width
        self._height = height
        self._fps = fps
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        if not self.mlx_ptr:
            raise RuntimeError("Can't initialize MLX")
        self.win = self.mlx.mlx_new_window(self.mlx_ptr, width, height, title)
        if not self.win:
            raise RuntimeError("Can't create MLX window")
        self._img = self.mlx.mlx_new_image(self.mlx_ptr, width, height)
        if not self._img:
            raise RuntimeError("Can't create MLX framebuffer image")
        data, _bpp, stride, _fmt = self.mlx.mlx_get_data_addr(self._img)
        self.screen = Surface(width, height, data=data, stride=stride,
                              is_screen=True)
        self.mlx.mlx_do_key_autorepeatoff(self.mlx_ptr)
        self.mlx.mlx_hook(self.win, _KEY_PRESS_EVENT, _KEY_PRESS_MASK,
                          self._on_key, None)
        self.mlx.mlx_hook(self.win, _DESTROY_NOTIFY, 0, self._on_close, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self._on_loop, None)

    def _on_key(self, keysym: int, _param: object) -> int:
        self._events.append(Event(
            EventType.KEYDOWN, key=keysym, char=keysym_to_char(keysym)))
        return 0

    def _on_close(self, _param: object) -> int:
        self.request_exit()
        return 0

    def _on_loop(self, _param: object) -> int:
        now = time.monotonic()
        if self._last_frame:
            elapsed = now - self._last_frame
            target = 1.0 / self._fps
            if elapsed < target:
                time.sleep(target - elapsed)
                now = time.monotonic()
                elapsed = now - self._last_frame
        else:
            elapsed = 0.0
        self._last_frame = now

        events = self._events
        self._events = []

        self._second_accum += elapsed
        while self._second_accum >= 1.0:
            self._second_accum -= 1.0
            events.append(Event(EventType.TIMER, timer_id=TIMER_GAME))
            events.append(Event(EventType.TIMER, timer_id=TIMER_GHOST))

        if self._frame_cb is not None:
            try:
                self._frame_cb(events)
            except SystemExit:
                self.request_exit()
            except Exception:
                import traceback
                traceback.print_exc()
                self.request_exit()
        if self._present_frames > 0:
            self._present()
            self._present_frames -= 1

        if self._should_exit:
            assert self.mlx is not None
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def _present(self) -> None:
        assert self.mlx is not None and self.screen is not None
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win, self._img, 0, 0)
        for x, y, color, text in self.screen.text_queue:
            packed = (color[0] << 16) | (color[1] << 8) | color[2]
            self.mlx.mlx_string_put(
                self.mlx_ptr, self.win, x, y, packed, text)

    def run(self, frame_cb: Callable[[list[Event]], None]) -> None:
        assert self.mlx is not None
        self._frame_cb = frame_cb
        self._last_frame = 0.0
        self.mlx.mlx_loop(self.mlx_ptr)

    def request_exit(self) -> None:
        self._should_exit = True

    def mark_dirty(self) -> None:
        """Present the next few frames (refreshes all swapchain buffers)."""
        self._present_frames = _PRESENT_REPEAT


app = MlxApp()
