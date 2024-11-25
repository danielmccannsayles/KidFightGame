import pygame as pg
from typing import Callable


COLOR_INACTIVE = pg.Color("lightskyblue3")
COLOR_ACTIVE = pg.Color("dodgerblue2")
FONT = pg.font.Font(None, 32)


class InputBox:
    def __init__(self, x, y, w, h, submit: Callable):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.active = False
        self.text = ""
        self.submit = submit
        self.draw_text()

    def handle_event(self, event):
        # Mouse down
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.update_active(True)
            else:
                self.update_active(False)

        # On any keydown event, trigger the box. I
        if event.type == pg.KEYDOWN:
            if not self.active:
                self.update_active(True)

            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pg.K_RETURN:
                self.submit(self.text)
                self.clear()

            else:
                self.text += event.unicode
            self.draw_text()

    def update_active(self, active: bool):
        self.active = active
        self.color = COLOR_ACTIVE if active else COLOR_INACTIVE

    def clear(self):
        self.text = ""
        self.draw_text()

    def draw_text(self):
        self.txt_surface = FONT.render(self.text, True, self.color)
        self.check_update_size()

    def check_update_size(self):
        text_width = self.txt_surface.get_width() + 10
        if text_width > self.rect.w:
            self.rect.w = text_width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)
