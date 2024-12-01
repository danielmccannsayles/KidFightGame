import pygame


"""
(row, column) is position on board
(x, y) is pixel coords from 0,0
"""


class Square:
    def __init__(self, row: int, column: int, width, height, x_offset, y_offset):
        self.occupying_piece = None
        self.highlight = False
        self.attack_highlight = False

        # Width and height of squares - consider calculating this here? as a property of the board?
        self.width = width
        self.height = height
        self.row = row
        self.column = column
        self.pos = (self.row, self.column)

        # Pixel coords
        # Note that column is actually how far it is in the x direction, while the row is how far it is in the y direction
        self.x = (self.column * width) + x_offset
        self.y = (self.row * height) + y_offset

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Color
        self.color = "light" if (row + column) % 2 == 0 else "dark"
        self.draw_color = (241, 211, 170) if self.color == "light" else (180, 126, 82)
        self.highlight_color = (
            (150, 255, 100) if self.color == "light" else (50, 220, 0)
        )

        # HP
        self.hp_color = (220, 20, 60)
        self.number_font = pygame.font.SysFont(None, 16)
        self.hp_rect = pygame.Rect(self.x, self.y, self.width, 10)

    def get_pos(self) -> tuple[int]:
        return self.pos

    def draw(self, display):
        if self.highlight:
            pygame.draw.rect(display, self.highlight_color, self.rect)
        elif self.attack_highlight:
            pygame.draw.rect(display, self.hp_color, self.rect)
        else:
            pygame.draw.rect(display, self.draw_color, self.rect)

        if self.occupying_piece != None:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)

            # HP bar
            if hasattr(self.occupying_piece, "hp"):
                pygame.draw.rect(display, self.hp_color, self.hp_rect)

                hptext = str(self.occupying_piece.hp)
                number_image = self.number_font.render(
                    hptext, True, (10, 10, 10), (255, 255, 255)
                )
                display.blit(number_image, centering_rect.topleft)
