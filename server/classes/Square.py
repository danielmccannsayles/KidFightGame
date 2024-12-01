from server.classes.DefaultPiece import DefaultPiece


class Square:
    """The squares class makes it easy to update the board"""

    def __init__(self, row: int, column: int):
        self.occupying_piece: DefaultPiece | None = None
        self.highlight = False

        self.row = row
        self.column = column
        self.pos = (self.row, self.column)

    def to_json(self):
        if self.occupying_piece != None:
            return self.occupying_piece.to_json()
        if self.highlight:
            return "H"
        return "."
