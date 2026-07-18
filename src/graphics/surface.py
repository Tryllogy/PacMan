from __future__ import annotations
import math
from typing import TYPE_CHECKING
from .color import Color
if TYPE_CHECKING:
    from .font import Text


class Rect:
    """A mutable rectangle with the pygame-like helpers the game uses."""

    def __init__(self, x: float, y: float, w: float, h: float) -> None:
        self.x: int = int(x)
        self.y: int = int(y)
        self.width: int = int(w)
        self.height: int = int(h)

    @property
    def left(self) -> int:
        return self.x

    @property
    def top(self) -> int:
        return self.y

    @property
    def right(self) -> int:
        return self.x + self.width

    @property
    def bottom(self) -> int:
        return self.y + self.height

    @property
    def centerx(self) -> int:
        return self.x + self.width // 2

    @property
    def centery(self) -> int:
        return self.y + self.height // 2

    @property
    def center(self) -> tuple[int, int]:
        return (self.centerx, self.centery)

    @property
    def topleft(self) -> tuple[int, int]:
        return (self.x, self.y)

    def colliderect(self, other: "Rect") -> bool:
        return (
            self.x < other.right
            and self.right > other.x
            and self.y < other.bottom
            and self.bottom > other.y
        )

    def collidepoint(self, point: tuple[int, int]) -> bool:
        px, py = point
        return self.x <= px < self.right and self.y <= py < self.bottom

    def copy(self) -> "Rect":
        return Rect(self.x, self.y, self.width, self.height)


class Surface:
    """A drawable RGBA (stored BGRA) pixel buffer."""

    def __init__(
        self,
        width: int,
        height: int,
        data: memoryview | bytearray | None = None,
        stride: int | None = None,
        is_screen: bool = False,
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.stride: int = stride if stride is not None else width * 4
        if data is not None:
            self.data: memoryview | bytearray = data
        else:
            self.data = bytearray(self.stride * height)
        self.is_screen: bool = is_screen
        self.text_queue: list[tuple[int, int, Color, str]] = []
        self._blank: bytes = b"\x00\x00\x00\xff" * (self.stride * height // 4)

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_size(self) -> tuple[int, int]:
        return (self.width, self.height)

    def get_rect(
        self,
        center: tuple[int, int] | None = None,
        topleft: tuple[int, int] | None = None,
    ) -> Rect:
        rect = Rect(0, 0, self.width, self.height)
        if center is not None:
            rect.x = center[0] - self.width // 2
            rect.y = center[1] - self.height // 2
        elif topleft is not None:
            rect.x, rect.y = topleft
        return rect

    def fill(self, color: Color) -> None:
        if color == (0, 0, 0):
            self.data[:] = self._blank
            if self.is_screen:
                self.text_queue.clear()
            return
        b, g, r = color[2], color[1], color[0]
        row = bytes((b, g, r, 255)) * self.width
        for y in range(self.height):
            off = y * self.stride
            self.data[off:off + self.width * 4] = row
        if self.is_screen:
            self.text_queue.clear()

    def draw_rect(
        self,
        color: Color,
        rect: Rect,
    ) -> None:
        x0 = max(0, rect.x)
        y0 = max(0, rect.y)
        x1 = min(self.width, rect.right)
        y1 = min(self.height, rect.bottom)
        if x1 <= x0 or y1 <= y0:
            return
        b, g, r = color[2], color[1], color[0]
        row = bytes((b, g, r, 255)) * (x1 - x0)
        for y in range(y0, y1):
            off = y * self.stride + x0 * 4
            self.data[off:off + (x1 - x0) * 4] = row

    def draw_circle(
        self,
        color: Color,
        center: tuple[int, int],
        radius: int,
    ) -> None:
        cx, cy = center
        b, g, r = color[2], color[1], color[0]
        for dy in range(-radius, radius + 1):
            y = cy + dy
            if y < 0 or y >= self.height:
                continue
            dx = int(math.sqrt(max(0, radius * radius - dy * dy)))
            x0 = max(0, cx - dx)
            x1 = min(self.width, cx + dx + 1)
            if x1 <= x0:
                continue
            off = y * self.stride + x0 * 4
            self.data[off:off + (x1 - x0) * 4] = bytes((b, g, r, 255)) * (
                x1 - x0)

    def blit(
        self,
        source: "Surface | Text",
        dest: tuple[int, int] | Rect,
    ) -> None:
        from .font import Text
        if isinstance(source, Text):
            if isinstance(dest, Rect):
                dx, dy = dest.x, dest.y
            else:
                dx, dy = int(dest[0]), int(dest[1])
            if self.is_screen:
                self.text_queue.append((dx, dy, source.color, source.text))
            return
        if isinstance(dest, Rect):
            dx, dy = dest.x, dest.y
        else:
            dx, dy = int(dest[0]), int(dest[1])
        self._blit_surface(source, dx, dy)

    def _blit_surface(self, src: "Surface", dx: int, dy: int) -> None:
        dst = self.data
        sd = src.data
        dstride = self.stride
        sstride = src.stride
        for sy in range(src.height):
            ty = dy + sy
            if ty < 0 or ty >= self.height:
                continue
            for sx in range(src.width):
                tx = dx + sx
                if tx < 0 or tx >= self.width:
                    continue
                so = sy * sstride + sx * 4
                a = sd[so + 3]
                if a == 0:
                    continue
                do = ty * dstride + tx * 4
                if a == 255:
                    dst[do] = sd[so]
                    dst[do + 1] = sd[so + 1]
                    dst[do + 2] = sd[so + 2]
                    dst[do + 3] = 255
                else:
                    ia = 255 - a
                    dst[do] = (sd[so] * a + dst[do] * ia) // 255
                    dst[do + 1] = (sd[so + 1] * a + dst[do + 1] * ia) // 255
                    dst[do + 2] = (sd[so + 2] * a + dst[do + 2] * ia) // 255
                    dst[do + 3] = 255
