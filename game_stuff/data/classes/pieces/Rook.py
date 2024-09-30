import pygame

from data.classes.Piece import Piece

# This is the main character piece
class Rook(Piece):
	def __init__(self, pos, color, board, movespeed, hp, attack_dmg):
		super().__init__(pos, color, board)

		if(self.color) == 'white':
			img_path = 'game_stuff/data/imgs/brutal-helm.png'
		else:
			img_path = 'game_stuff/data/imgs/orc-head.png'

		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.square_width - 20, board.square_height - 20))

		self.notation = 'R'


		self.movespeed = movespeed
		self.max_hp = hp
		self.hp = self.max_hp

		self.attack_dmg = attack_dmg
		

	def get_possible_moves(self, board):
		output = []
		moves_north = []
		y = range(self.y - self.movespeed, self.y + self.movespeed + 1)
		x = range(self.x - self.movespeed, self.x + self.movespeed + 1)
		print(*x, sep=",")
		for t in y:
			if (t>=0) and (t<8) and not (t==self.y):
				moves_north.append(board.get_square_from_pos(
				(self.x, t)))
		output.append(moves_north)
		moves_east = []
		for t in x:
			if (t>=0) and (t<8) and not (t==self.x):
				moves_east.append(board.get_square_from_pos(
					(t, self.y)
				))
		output.append(moves_east)
		return output
