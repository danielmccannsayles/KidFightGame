## Typing Hack - allow imports for type safety w/o causing circular..
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_stuff.classes.Square import Square
    from game_stuff.classes.Board import Board


import pygame
from game_stuff.classes.pieces.DefaultPiece import DefaultPiece
import random

# Needed for relative image import
import os

current_dir = os.path.dirname(__file__)


# Home Base Class
class Base:
    def __init__(self, top_left: tuple[int], color, board: Board):
        self.color = color
        self.top_left = top_left
        self.board = board

        self.pieces = self._setup_pieces()
        self.spawns = self._setup_spawns()

        # For testing highlight spawns
        for spawn_square in self.spawns:
            spawn_square.highlight = True

    def _setup_pieces(self) -> list[DefaultPiece]:
        # Images
        if self.color == "white":
            img_path = f"{current_dir}/../../imgs/w_rook.png"
        else:
            img_path = f"{current_dir}/../../imgs/b_rook.png"
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(
            img, (self.board.square_width - 20, self.board.square_height - 20)
        )

        # Pieces
        pieces: list[DefaultPiece] = []
        row, column = self.top_left
        for r in [row, row + 1]:
            for c in [column, column + 1]:
                pieces.append(DefaultPiece((r, c), self.color, img))

        # Add to square object
        for piece in pieces:
            square = self.board.get_square_from_board_pos(piece.pos)
            square.occupying_piece = piece
        return pieces

    def _setup_spawns(self) -> list[Square]:
        row, column = self.top_left
        positions = set()
        print("row, column", row, column)

        # Top row - check if out of bounds
        if row > 0:
            print("not out of bounds on top")
            for c in range(column - 1, column + 3):
                positions.add((row - 1, c))

        # Bottom row - check if out of bounds (3: 2 for size + 1 for 0 indexed)
        if row + 3 <= self.board.rows:
            print("not out of bounds on bottom")
            for c in range(column - 1, column + 3):
                positions.add((row + 2, c))

        # Left and right columns
        for r in range(row, row + 2):
            positions.add((r, column - 1))  # Left column
            positions.add((r, column + 2))  # Right column

        print(positions)

        spawns: list[Square] = []
        for pos in positions:
            square = self.board.get_square_from_board_pos(pos)
            spawns.append(square)

        return spawns

    # Check for non occupied spawns..
    def get_spawn(self):
        return random.choice(self.spawns)
