## Typing Hack - allow imports for type safety w/o causing circular..
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from server.classes.Board import Board


from server.classes.DefaultPiece import DefaultPiece
import random


class Base:
    def __init__(self, top_left: list[tuple[int, int]], color, board: Board):
        self.color = color
        self.top_left = top_left
        self.board = board

        self.pieces = self._setup_pieces()
        self.spawns = self._setup_spawns()

    def _setup_pieces(self) -> list[DefaultPiece]:
        if self.color == "white":
            piece_type = "WB"
        else:
            piece_type = "BB"

        # Pieces
        pieces: list[DefaultPiece] = []
        row, column = self.top_left
        for r in [row, row + 1]:
            for c in [column, column + 1]:
                pieces.append(DefaultPiece((r, c), self.color, piece_type))

        # Add to board
        for piece in pieces:
            self.board.add_piece_safe(piece.pos, piece)
        return pieces

    def _setup_spawns(self) -> list[list[tuple[int, int]]]:
        """Mathematically gets positions around base using the row length. Returns tuple of positions."""
        row, column = self.top_left
        positions = set()

        # Top row - check if out of bounds
        if row > 0:
            for c in range(column - 1, column + 3):
                positions.add((row - 1, c))

        # Bottom row - check if out of bounds (3: 2 for size + 1 for 0 indexed)
        if row + 3 <= self.board.rows:
            for c in range(column - 1, column + 3):
                positions.add((row + 2, c))

        # Left and right columns
        for r in range(row, row + 2):
            positions.add((r, column - 1))  # Left column
            positions.add((r, column + 2))  # Right column

        return positions

    def get_open_spawn_pos(self):
        """Return random open spawn position"""
        open_squares = [
            spawn
            for spawn in self.spawns
            if not self.board.check_if_occupied_pos(spawn)
        ]
        return random.choice(open_squares)
