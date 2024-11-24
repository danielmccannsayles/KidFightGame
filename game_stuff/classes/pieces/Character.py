import pygame
from game_stuff.classes.pieces.DefaultPiece import DefaultPiece

# Needed for relative image import
import os

current_dir = os.path.dirname(__file__)


# This is the main character piece
class Character(DefaultPiece):
    def __init__(self, pos, color, board, movespeed, hp, attack_dmg, rows):
        if (color) == "white":
            img_path = f"{current_dir}/../../imgs/brutal-helm.png"
        else:
            img_path = f"{current_dir}/../../imgs/orc-head.png"

        img = pygame.image.load(img_path)
        img = pygame.transform.scale(
            img, (board.square_width - 20, board.square_height - 20)
        )

        # DO this down here to init img
        super().__init__(pos, color, img)

        self.movespeed = movespeed
        self.max_hp = hp
        self.hp = self.max_hp

        self.attack_dmg = attack_dmg
        self.rows = rows
        self.board = board

    def get_possible_moves(self):
        output = []

        # What is this??
        y = range(self.column - self.movespeed, self.column + self.movespeed + 1)
        x = range(self.row - self.movespeed, self.row + self.movespeed + 1)

        # What is hapening? I think we are checking that we can move.. should move this to board
        moves_north = []
        for t in y:
            if (t >= 0) and (t < self.rows) and not (t == self.column):
                moves_north.append(self.board.get_square_from_board_pos((self.row, t)))
        output.append(moves_north)

        # Same.. think we are
        moves_east = []
        for t in x:
            if (t >= 0) and (t < self.rows) and not (t == self.row):
                moves_east.append(
                    self.board.get_square_from_board_pos((t, self.column))
                )
        output.append(moves_east)
        return output
