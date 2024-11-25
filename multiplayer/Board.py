from multiplayer.Square import Square


class Board:
    def to_dict(self):
        return {
            "squares": [square.to_dict() for square in self.squares],
        }

    # TODO: what else needs to be updated?
    def update_board(self, data):
        """Update board from square json data"""
        self.squares = [Square.from_dict(d) for d in data["squares"]]

    # IF I ned to re-init from object..
    # @classmethod
    # def from_dict(cls, data):
    #     board = cls()
    #     board.squares = [Square.from_dict(d) for d in data["squares"]]
    #     return board
