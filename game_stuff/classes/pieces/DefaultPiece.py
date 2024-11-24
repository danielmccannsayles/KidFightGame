## Typing Hack - allow imports for type safety w/o causing circular..
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_stuff.classes.Square import Square
    from game_stuff.classes.Board import Board


class DefaultPiece:
    def __init__(self, pos, color, img):
        self.pos = pos
        self.row = pos[0]
        self.column = pos[1]
        self.color = color
        self.has_moved = False
        self.img = img

    def set_pos(self, pos):
        self.pos = pos
        self.row = pos[0]
        self.column = pos[1]

    def move(self, board: Board, square: Square):
        for i in board.squares:
            i.highlight = False
            i.attack_highlight = False

        # Move to a square
        if square in self.get_moves():
            self._move_to_square(board, square)
            board.selected_piece = None
            return True

        # Attack (if successful, move)
        elif square in self.get_valid_attacks():
            square.occupying_piece.hp = square.occupying_piece.hp - self.attack_dmg
            if square.occupying_piece.hp <= 0:
                self._move_to_square(board, square)

            board.selected_piece = None
            return True

        else:
            board.selected_piece = None
            return False

    def _move_to_square(self, board: Board, square: Square):
        # Remove from old square
        prev_square = board.get_square_from_board_pos(self.pos)
        prev_square.occupying_piece = None

        # Add to new square
        self.set_pos(square.get_pos())
        square.occupying_piece = self
        self.has_moved = True

    def get_moves(self):
        output = []
        for direction in self.get_possible_moves():
            for square in direction:
                if square.occupying_piece is None:
                    output.append(square)

        return output

    def get_valid_attacks(self):
        output = []
        for direction in self.get_possible_moves():
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color != self.color:
                        output.append(square)

        return output
