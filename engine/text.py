import pygame
from engine.colors import *

class Text:
    def __init__(self, text, font_name, font_color=WHITE, font_percent_size=0.2, bold=False, italic=False, bg_color=None):
        self.text = text
        self.font_name = font_name
        self.font_color = font_color
        self.font_percent_size = font_percent_size
        self.bold = bold
        self.italic = italic
        self.bg_color = bg_color

    def get_text(self, window: pygame.Surface) -> pygame.Surface:
        font = pygame.font.SysFont(
            self.font_name,
            int(self.font_percent_size * window.get_size()[1]),
            self.bold, self.italic)

        return font.render(self.text, True, self.font_color, self.bg_color)


