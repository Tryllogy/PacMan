from .scene import Scene
import pygame
from .. import constant


class MainScene(Scene):

    def draw(
        self,
        mouse_pos: tuple[int, int]
    ) -> None:
        super().draw(mouse_pos)
        self.place_txt("Play", mouse_pos, -150, -100)
        self.place_txt("View highscores", mouse_pos, -150, -50)
        self.place_txt("Instructions", mouse_pos, -150, 0)
        self.place_txt("Exit", mouse_pos, -150, 50)

    def place_txt(
        self,
        txt_str: str,
        mouse_pos: tuple[int, int],
        off_x: int,
        off_y: int,
    ) -> None:
        x, y = self.middle_screen
        color: tuple[int, int, int] = constant.TEXT_COLOR_BASE
        color_hover: tuple[int, int, int] = constant.TEXT_COLOR_HOVER

        txt_render: pygame.Surface = self.font.render(
            txt_str, True, color)
        txt_dim: tuple[int, int] = (
            txt_render.get_width(),
            txt_render.get_height()
        )
        txt_pos: tuple[int, int] = (x + off_x, y + off_y)
        if self.hover_text(
            txt_dim,
            mouse_pos,
            txt_pos
        ):
            txt_render: pygame.Surface = self.font.render(
                txt_str, True, color_hover)
        self.screen.blit(txt_render, (x + off_x, y + off_y))
