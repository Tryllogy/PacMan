from __future__ import annotations
from typing import TYPE_CHECKING
from .surface import Surface
if TYPE_CHECKING:
    from .app import MlxApp


def load_image(app: "MlxApp", path: str) -> Surface:
    """Load ``path`` (PNG) into an off-screen Surface via MLX."""
    assert app.mlx is not None, "MLX must be initialized before loading images"
    img_ptr, width, height = app.mlx.mlx_png_file_to_image(app.mlx_ptr, path)
    if not img_ptr:
        raise FileNotFoundError(f"Could not load image: {path}")
    data, _bpp, stride, _fmt = app.mlx.mlx_get_data_addr(img_ptr)
    surf = Surface(width, height)
    row_bytes = width * 4
    for y in range(height):
        src_off = y * stride
        dst_off = y * row_bytes
        surf.data[dst_off:dst_off + row_bytes] = data[
            src_off:src_off + row_bytes]
    app.mlx.mlx_destroy_image(app.mlx_ptr, img_ptr)
    return surf


def scale(surface: Surface, size: tuple[int, int]) -> Surface:
    """Nearest-neighbour scale to ``(width, height)``."""
    new_w, new_h = int(size[0]), int(size[1])
    out = Surface(new_w, new_h)
    src = surface.data
    dst = out.data
    sstride = surface.stride
    if new_w <= 0 or new_h <= 0:
        return out
    x_map = [(x * surface.width) // new_w for x in range(new_w)]
    for y in range(new_h):
        sy = (y * surface.height) // new_h
        srow = sy * sstride
        drow = y * new_w * 4
        for x in range(new_w):
            so = srow + x_map[x] * 4
            do = drow + x * 4
            dst[do:do + 4] = src[so:so + 4]
    return out


def rotate(surface: Surface, angle: int) -> Surface:
    """Rotate by a multiple of 90 degrees, counter-clockwise (pygame-like)."""
    angle %= 360
    if angle == 0:
        return surface
    w, h = surface.width, surface.height
    src = surface.data
    sstride = surface.stride

    def pixel(sx: int, sy: int) -> bytes:
        o = sy * sstride + sx * 4
        return bytes(src[o:o + 4])

    if angle == 90:
        out = Surface(h, w)
        for sy in range(h):
            for sx in range(w):
                dx, dy = sy, w - 1 - sx
                do = dy * out.stride + dx * 4
                out.data[do:do + 4] = pixel(sx, sy)
        return out
    if angle == 180:
        out = Surface(w, h)
        for sy in range(h):
            for sx in range(w):
                dx, dy = w - 1 - sx, h - 1 - sy
                do = dy * out.stride + dx * 4
                out.data[do:do + 4] = pixel(sx, sy)
        return out
    if angle == 270:
        out = Surface(h, w)
        for sy in range(h):
            for sx in range(w):
                dx, dy = h - 1 - sy, sx
                do = dy * out.stride + dx * 4
                out.data[do:do + 4] = pixel(sx, sy)
        return out
    return surface
