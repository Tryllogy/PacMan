import pygame
from ... import constant

color = tuple[int, int, int]


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        text: str,
        callback: callable,
        font: pygame.font.Font,
    ) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, w, h)
        self.text: str = text
        self.callback: callable = callback
        self.font: pygame.font.Font = font
        self.base_color: color = constant.BUTTON_COLOR_BASE
        self.hover_color: color = constant.BUTTON_COLOR_HOVER
        self.hovered: bool = False

    def draw(
        self,
        screen
    ) -> None:
        color = self.hover_color if self.hovered else self.base_color

        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        text_surf = self.font.render(self.text, True, constant.TEXT_COLOR_BASE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(
        self,
        event
    ) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.callback()
