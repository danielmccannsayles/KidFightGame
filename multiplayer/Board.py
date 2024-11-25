from multiplayer.Square import Square
from multiplayer.Piece import Piece, PieceData, is_piece_data


"""
We're going to communicate using a list.
This list will be the board. It will have objects

e.g:
['.', '.', '{}', '{}',]

'.' are empty
'H' is highlight? TODO: do we want to continue highlighting?
WB, BB, WC, BC are piece types
"""


class Board:
    def __init__(self, size: int, x_offset, y_offset, rows: int):
        self.width = size
        self.height = size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.square_size = size // rows
        self.rows = rows
        self.squares: list[Square] = self.generate_squares()

    def update_board(self, board_list: list[str | PieceData]):
        """Update board from json data. Clear everything on squares, then re-add"""
        if len(self.squares) != len(board_list):
            print("This should not happen.. mismatch btwn server and client")

        for data, square in zip(board_list, self.squares):
            square.occupying_piece = None
            square.highlight = False

            if is_piece_data(data):
                piece = Piece(self.square_size, data)
                square.occupying_piece = piece

            elif data == "H":
                square.highlight = True

    def draw(self, display):
        for square in self.squares:
            square.draw(display)

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

    # Only needed on server
    def to_dict(self):
        return {
            "squares": [square.to_dict() for square in self.squares],
        }

    # IF I ned to re-init from object..
    # @classmethod
    # def from_dict(cls, data):
    #     board = cls()
    #     board.squares = [Square.from_dict(d) for d in data["squares"]]
    #     return board
