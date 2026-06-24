import pygame
from .. import constant


class Button:
    def __init__(
        self,
        x,
        y,
        w,
        h,
        text,
        callback,
        font,
    ) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        self.font = font
        self.base_color = constant.BUTTON_COLOR_BASE
        self.hover_color = constant.BUTTON_COLOR_HOVER
        self.txt_color = constant.TEXT_COLOR_BASE
        self.hovered = False

    def draw(
        self,
        screen
    ) -> None:
        if self.clicked and pygame.time.get_ticks() - self.click_timer < 100:
            color = self.click_color
        else:
            color = self.hover_color if self.hovered else self.base_color

        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(
        self,
        event
    ) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.clicked = True
            self.click_timer = pygame.time.get_ticks()
            self.callback()
