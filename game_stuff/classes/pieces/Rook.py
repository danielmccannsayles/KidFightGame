import pygame
from game_stuff.classes.Piece import Piece

# Needed for relative image import
import os

current_dir = os.path.dirname(__file__)


# This is the main character piece
class Rook(Piece):
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
        moves_north = []
        y = range(self.y - self.movespeed, self.y + self.movespeed + 1)
        x = range(self.x - self.movespeed, self.x + self.movespeed + 1)

        for t in y:
            if (t >= 0) and (t < self.rows) and not (t == self.y):
                moves_north.append(self.board.get_square_from_pos((self.x, t)))
        output.append(moves_north)
        moves_east = []
        for t in x:
            if (t >= 0) and (t < self.rows) and not (t == self.x):
                moves_east.append(self.board.get_square_from_pos((t, self.y)))
        output.append(moves_east)
        return output
