from server.classes.DefaultPiece import DefaultPiece
from server.classes.Base import Base
from server.classes.Character import Character
from server.classes.Square import Square


class Board:
    def __init__(self, rows: int):
        self.rows = rows
        self.squares: list[list[Square]] = self.generate_squares()
        self.bases = self.make_bases()
        self.characters: dict[str, list[Character]] = {"black": [], "white": []}

    def to_json(self):
        """Got through the squares and serialize each of them and return it. Returns a flattened list"""
        flat_squares = [square for columns in self.squares for square in columns]
        json_list = [square.to_json() for square in flat_squares]

        return json_list

    def generate_squares(self):
        output: list[list[Square]] = []
        for row in range(self.rows):
            inner_list = []
            for column in range(self.rows):
                inner_list.append(Square(row, column))

            output.append(inner_list)
        return output

    # Each base is 2x2 squares. Assumes rows are even
    def make_bases(self):
        column = int(self.rows / 2 - 1)
        bottom_row = self.rows - 2
        top_row = 0

        top_base_top_left = top_row, column
        bottom_base_top_left = bottom_row, column

        w_base = Base(top_base_top_left, "white", self)
        b_base = Base(bottom_base_top_left, "black", self)
        return {"white": w_base, "black": b_base}

    def add_piece_safe(self, pos: tuple[int], piece: DefaultPiece):
        """Add the given piece to the given position on the board. Fails quietly w/ console log. Sets the pieces position to square position"""
        square = self.get_pos(pos)
        if not square:
            print("invalid square", pos)
            return
        if self.check_if_occupied(square):
            print("already occupied")
            return

        square.occupying_piece = piece
        piece.set_pos((square.row, square.column))

    def move_piece_to_pos(self, new_pos: tuple[int], piece: DefaultPiece):
        """Move piece and clear previous square"""
        new_square = self.get_pos(new_pos)
        if not new_square:
            print("invalid square")
            return
        if self.check_if_occupied(new_square):
            print("already occupied")
            return

        self.clear_square_pos(piece.pos)
        new_square.occupying_piece = piece
        piece.set_pos((new_square.row, new_square.column))

    def clear_square_pos(self, pos: tuple[int]):
        square = self.get_pos(pos)
        if square:
            square.occupying_piece = None

    def check_if_occupied(self, square: Square):
        return square.occupying_piece != None

    def check_if_occupied_pos(self, pos: tuple[int]):
        square = self.get_pos(pos)
        if square:
            return square.occupying_piece != None

    def get_pos(self, pos: tuple[int]):
        row = pos[0]
        column = pos[1]
        if row < 0 or row >= self.rows:
            return False
        if column < 0 or column >= self.rows:
            return False
        return self.squares[pos[0]][pos[1]]

    def set_highlight(self, positions: list[tuple[int]]):
        for pos in positions:
            square = self.get_pos(pos)

            if square:
                square.highlight = True

    def clear_highlight(self):
        for _, _, value in self._flat_iterate():
            value.highlight = False

    def reset_board(self):
        for _, _, value in self._flat_iterate():
            value.occupying_piece = None
            value.highlight = False

        self.bases = self.make_bases()

    def _flat_iterate(self):
        """Flat iterate over squares"""
        for i, row in enumerate(self.squares):
            for j, value in enumerate(row):
                yield i, j, value

    def print_characters(self):
        for k, v in self.characters.items():
            print(f"{k}: {v}")
