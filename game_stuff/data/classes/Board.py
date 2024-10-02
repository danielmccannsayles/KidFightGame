import pygame

from data.classes.Square import Square
from data.classes.pieces.Rook import Rook


# Only needs rows since we make a square boarc
class Board:
    def __init__(self, width, height, x_offset, y_offset, rows):
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.square_width = width // rows
        self.square_height = height // rows
        self.selected_piece = None
        self.turn = "white"

        self.rows = rows

        self.squares: list[Square] = self.generate_squares()

    def generate_squares(self):
        output = []
        for y in range(self.rows):
            for x in range(self.rows):
                output.append(
                    Square(
                        x,
                        y,
                        self.square_width,
                        self.square_height,
                        self.x_offset,
                        self.y_offset,
                    )
                )

        return output

    # TODO: Add ability to add character (will update spot on board w/ new character)
    def add_character(self, board_x, board_y):
        x = board_x // self.square_width
        y = board_y // self.square_height
        piece = Rook((x, y), "white", self, 2, 10, 2, self.rows)
        square = self.get_square_from_pos((x, y))
        if square.occupying_piece:
            print("already occupied")
        else:
            square.occupying_piece = piece

    def reset_board(self):
        for square in self.squares:
            square.occupying_piece = None

    def handle_click(self, board_x, board_y):
        x = board_x // self.square_width
        y = board_y // self.square_height
        print(x, y)
        clicked_square = self.get_square_from_pos((x, y))
        print(clicked_square)
        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece

        elif self.selected_piece.move(self, clicked_square):
            self.turn = "white" if self.turn == "black" else "black"

        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece

    def get_square_from_pos(self, pos) -> Square:
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece

    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_moves(self):
                square.highlight = True
            x = self.selected_piece.get_valid_attacks(self)
            for square in x:
                square.attack_highlight = True

        for square in self.squares:
            square.draw(display)
