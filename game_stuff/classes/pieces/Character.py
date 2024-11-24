## Typing Hack - allow imports for type safety w/o causing circular..
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_stuff.classes.Board import Board

import pygame
from game_stuff.classes.pieces.DefaultPiece import DefaultPiece

# Needed for relative image import
import os

current_dir = os.path.dirname(__file__)


# This is the main character piece
class Character(DefaultPiece):
    def __init__(self, pos, color, board: Board, movespeed, hp, attack_dmg):
        if (color) == "white":
            img_path = f"{current_dir}/../../imgs/brutal-helm.png"
        else:
            img_path = f"{current_dir}/../../imgs/orc-head.png"

        img = pygame.image.load(img_path)
        img = pygame.transform.scale(
            img, (board.square_size - 20, board.square_size - 20)
        )

        # DO this down here to init img
        super().__init__(pos, color, img)

        self.movespeed = movespeed
        self.max_hp = hp
        self.hp = self.max_hp

        self.attack_dmg = attack_dmg
        self.board = board

    def get_possible_moves(self):
        output = []

        # What is this??
        vertical_range = range(
            self.row - self.movespeed, self.column + self.movespeed + 1
        )
        horizontal_range = range(
            self.column - self.movespeed, self.row + self.movespeed + 1
        )

        # What is hapening? I think we are checking that we can move.. should move this to board
        moves_vertical = []
        for t in vertical_range:
            if (t >= 0) and (t < self.board.rows) and not (t == self.column):
                moves_vertical.append(
                    self.board.get_square_from_board_pos((self.row, t))
                )
        output.append(moves_vertical)

        # Same.. think we are
        moves_horizontal = []
        for t in horizontal_range:
            if (t >= 0) and (t < self.board.rows) and not (t == self.row):
                moves_horizontal.append(
                    self.board.get_square_from_board_pos((t, self.column))
                )
        output.append(moves_horizontal)
        return output
