import pygame
from game_stuff.classes.pieces.DefaultPiece import DefaultPiece

# Needed for relative image import
import os

current_dir = os.path.dirname(__file__)


# Home Base Class
class Base:
    def __init__(self, top_left, color, board):
        self.color = color
        self.top_left = top_left
        self.board = board

        if self.color == "white":
            img_path = f"{current_dir}/../../imgs/w_rook.png"
        else:
            img_path = f"{current_dir}/../../imgs/b_rook.png"

        # Pass in imgs to pieces
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(
            img, (board.square_width - 20, board.square_height - 20)
        )

        pieces: list[DefaultPiece] = []
        print(f"making base color {color}")

        # Surely there's a more elegant way than this..
        for x in [top_left[0], top_left[0] + 1]:
            for y in [top_left[1], top_left[1] + 1]:
                print(f"{x,y}")
                pieces.append(DefaultPiece((x, y), self.color, img))

        # Add the pieces to the board
        for piece in pieces:
            square = board.get_square_from_pos(piece.pos)
            square.occupying_piece = piece

        self.pieces = pieces

    # TODO: get possible spawns around base
    def get_possible_moves(self):
        output = []
        moves_north = []
        y = range(self.y - self.movespeed, self.y + self.movespeed + 1)
        x = range(self.x - self.movespeed, self.x + self.movespeed + 1)
        print(*x, sep=",")
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
