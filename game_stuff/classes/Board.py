from game_stuff.classes.Square import Square
from game_stuff.classes.pieces.Character import Character
from game_stuff.classes.pieces.Base import Base


# Only needs rows since we make a square board
class Board:
    def __init__(self, width, height, x_offset, y_offset, rows: int):
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
        self.bases = self.make_bases()

    def generate_squares(self):
        output = []
        for row in range(self.rows):
            for column in range(self.rows):
                output.append(
                    Square(
                        row,
                        column,
                        self.square_width,
                        self.square_height,
                        self.x_offset,
                        self.y_offset,
                    )
                )

        return output

    # Set to make two bases. One on the top, one on the bottom. Each base is 2x2 squares.
    # Assumes rows are even
    def make_bases(self):
        column = int(self.rows / 2 - 1)
        bottom_row = self.rows - 2
        top_row = 0

        top_base_top_left = column, top_row
        bottom_base_top_left = column, bottom_row

        top_base = Base(top_base_top_left, "white", self)
        bot_base = Base(bottom_base_top_left, "black", self)
        return top_base, bot_base

    def add_character(self, board_x, board_y, piece: Character):
        x = board_x // self.square_width
        y = board_y // self.square_height

        # Update piece w/ x, y
        piece.set_pos((x, y))

        square = self.get_square_from_board_pos((x, y))
        if square.occupying_piece:
            print("already occupied")
        else:
            square.occupying_piece = piece

    def reset_board(self):
        for square in self.squares:
            square.occupying_piece = None
        self.bases = self.make_bases()

    def handle_click(self, board_x, board_y):
        x = board_x // self.square_width
        y = board_y // self.square_height
        clicked_square = self.get_square_from_board_pos((x, y))
        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.turn:
                    self.selected_piece = clicked_square.occupying_piece

        elif self.selected_piece.move(self, clicked_square):
            self.turn = "white" if self.turn == "black" else "black"

        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece

    # row, column
    def get_square_from_board_pos(self, pos) -> Square:
        for square in self.squares:
            if (square.row, square.column) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos):
        return self.get_square_from_board_pos(pos).occupying_piece

    def draw(self, display):
        if self.selected_piece is not None:
            self.get_square_from_board_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_moves():
                square.highlight = True
            x = self.selected_piece.get_valid_attacks()
            for square in x:
                square.attack_highlight = True

        for square in self.squares:
            square.draw(display)
