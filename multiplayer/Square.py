import pygame
from multiplayer.Piece import Piece

COLORS = {"light": (241, 211, 170), "dark": (180, 126, 82)}
HIGHLIGHT = {"light": (150, 255, 100), "dark": (50, 220, 0)}


class Square:
    """Squares are drawn on the board. They know their own pixel positions. They do not update -"""

    def __init__(self, row: int, column: int, width, height, x_offset, y_offset):
        self.occupying_piece: Piece | None = None
        self.highlight = False

        # Width and height of squares - consider calculating this here? as a property of the board?
        self.width = width
        self.height = height
        self.row = row
        self.column = column
        self.pos = (self.row, self.column)

        # Pixel coords
        self.x = (self.column * width) + x_offset
        self.y = (self.row * height) + y_offset
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Color
        # TODO: move this outside, have it be passed in
        type = "light" if (row + column) % 2 == 0 else "dark"
        self.draw_color = COLORS[type]
        self.highlight_color = HIGHLIGHT[type]

        # HP
        self.hp_color = (220, 20, 60)
        self.number_font = pygame.font.SysFont(None, 16)
        self.hp_rect = pygame.Rect(self.x, self.y, self.width, 10)

    def draw(self, display):
        """Draw highlight or draw player or draw nothing"""
        color = self.highlight_color if self.highlight else self.draw_color
        pygame.draw.rect(display, color, self.rect)

        piece = self.occupying_piece

        if piece != None:
            centering_rect = piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(piece.img, centering_rect.topleft)

            # HP bar - if exists and not equal to none
            if hasattr(piece, "hp") and piece.hp:
                pygame.draw.rect(display, self.hp_color, self.hp_rect)

                hptext = str(piece.hp)
                number_image = self.number_font.render(
                    hptext, True, (10, 10, 10), (255, 255, 255)
                )
                display.blit(number_image, centering_rect.topleft)
