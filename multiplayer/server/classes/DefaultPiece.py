class DefaultPiece:
    def __init__(self, pos, color, piece_type):
        self.pos = pos
        self.row = pos[0]
        self.column = pos[1]
        self.color = color
        self.piece_type = piece_type

    def set_pos(self, pos):
        self.pos = pos
        self.row = pos[0]
        self.column = pos[1]

    # TODO -
    def to_json(self):
        pass
