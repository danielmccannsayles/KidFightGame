class DefaultPiece:
    def __init__(self, pos, color, pieceType):
        self.pos = pos
        self.row = pos[0]
        self.column = pos[1]
        self.color = color
        self.type = pieceType

    def set_pos(self, pos):
        self.pos = pos
        self.row = pos[0]
        self.column = pos[1]
