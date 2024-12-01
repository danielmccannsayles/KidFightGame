from numpy import character
from game_stuff.classes.Square import Square
from game_stuff.classes.pieces.Character import Character
from game_stuff.classes.pieces.Base import Base


# Only needs rows since we make a square board
# NOTE on positioning system. rows and columns start at 0,0 in the top left corner.
# Rows are calculated from the y position
class Board:
    def __init__(self, size: int, x_offset, y_offset, rows: int):
        self.width = size
        self.height = size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.square_size = size // rows
        self.selected_piece = None

        self.rows = rows
        self.squares: list[Square] = self.generate_squares()
        self.bases = self.make_bases()
        self.characters: dict[str, list[Character]] = {"black": [], "white": []}

    def print_characters(self):
        for k, v in self.characters.items():
            print(f"{k}: {v}")

    def generate_squares(self):
        output = []
        for row in range(self.rows):
            for column in range(self.rows):
                output.append(
                    Square(
                        row,
                        column,
                        self.square_size,
                        self.square_size,
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

        top_base_top_left = top_row, column
        bottom_base_top_left = bottom_row, column

        w_base = Base(top_base_top_left, "white", self)
        b_base = Base(bottom_base_top_left, "black", self)
        return {"white": w_base, "black": b_base}

    def reset_board(self):
        for square in self.squares:
            square.occupying_piece = None
        self.bases = self.make_bases()

    # row, column
    def get_square_from_board_pos(self, pos: tuple[int]) -> Square:
        for square in self.squares:
            if square.pos == pos:
                return square

    def add_character(self, square: Square, piece: Character, color: str):
        if square.occupying_piece:
            print("already occupied")
        else:
            piece.set_pos((square.row, square.column))
            square.occupying_piece = piece
            self.characters[color].append(piece)

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
        print(self.characters)

    def clear_highlight(self):
        for square in self.squares:
            square.highlight = False
            square.attack_highlight = False

    def remove_character(self, toRemove):
        characters = []
        for key, value in self.characters.items():
            if toRemove.occupying_piece in value:
                print("helpmeeeeeeeeee")
                value.remove(toRemove.occupying_piece)
                toRemove.occupying_piece = None
    # Deprecated click methods
    # def handle_click(self, board_x, board_y):
    #     x = board_x // self.square_size
    #     y = board_y // self.square_size
    #     clicked_square = self.get_square_from_board_pos((x, y))
    #     if self.selected_piece is None:
    #         if clicked_square.occupying_piece is not None:
    #             if clicked_square.occupying_piece.color == self.turn:
    #                 self.selected_piece = clicked_square.occupying_piece

    #     elif self.selected_piece.move(self, clicked_square):
    #         self.turn = "white" if self.turn == "black" else "black"

    #     elif clicked_square.occupying_piece is not None:
    #         if clicked_square.occupying_piece.color == self.turn:
    #             self.selected_piece = clicked_square.occupying_piece
