Color = tuple[int, int, int]


def rgb_to_int(color: Color, alpha: int = 255) -> int:
    """Pack an ``(r, g, b)`` tuple into a ``0xAARRGGBB`` integer."""
    r, g, b = color
    return (alpha << 24) | (r << 16) | (g << 8) | b


def rgb_to_bgra(color: Color, alpha: int = 255) -> bytes:
    """Pack an ``(r, g, b)`` tuple into ``B, G, R, A`` bytes (MLX format 0)."""
    r, g, b = color
    return bytes((b, g, r, alpha))
