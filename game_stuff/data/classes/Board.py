import pygame

from data.classes.Square import Square
from data.classes.pieces.Rook import Rook


class Board:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.square_width = width // 8
		self.square_height = height // 8
		self.selected_piece = None
		self.turn = 'white'

		self.config = [
			['','','','','','','',''],
			['','','bR','','','bR','',''],
			['','','','','','','',''],
			['','','','','wR','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','wR','','','','',''],
		]

		self.squares: list[Square] = self.generate_squares()

		self.setup_board()

	def generate_squares(self):
		output = []
		for y in range(8):
			for x in range(8):
				output.append(
					Square(
						x,
						y,
						self.square_width,
						self.square_height
					)
				)

		return output


	def setup_board(self):
		for y, row in enumerate(self.config):
			for x, piece in enumerate(row):
				if piece != '':
					square = self.get_square_from_pos((x, y))

					if piece[1] == 'R':
						square.occupying_piece = Rook(
							(x, y),
							'white' if piece[0] == 'w' else 'black',
							self,
							1,
							10,
							2
						)


	# TODO: Add ability to add character (will update spot on board w/ new character)
	def add_character(self, x, y, piece: Rook):
		square = self.get_square_from_pos((x, y))
		square.occupying_piece =  piece


	def handle_click(self, mx, my, x_offset, y_offset):
		if(mx >= x_offset) and (my >= y_offset):		
			x = (mx - x_offset) // self.square_width
			y = (my - y_offset) // self.square_height
			print(x, y)
			clicked_square = self.get_square_from_pos((x, y))
			print(clicked_square)
			if self.selected_piece is None:
				if clicked_square.occupying_piece is not None:
					if clicked_square.occupying_piece.color == self.turn:
						self.selected_piece = clicked_square.occupying_piece

			elif self.selected_piece.move(self, clicked_square):
				self.turn = 'white' if self.turn == 'black' else 'black'

			elif clicked_square.occupying_piece is not None:
				if clicked_square.occupying_piece.color == self.turn:
					self.selected_piece = clicked_square.occupying_piece


	def is_in_check(self, color, board_change=None): # board_change = [(x1, y1), (x2, y2)]
		output = False
		king_pos = None

		changing_piece = None
		old_square = None
		new_square = None
		new_square_old_piece = None

		if board_change is not None:
			for square in self.squares:
				if square.pos == board_change[0]:
					changing_piece = square.occupying_piece
					old_square = square
					old_square.occupying_piece = None
			for square in self.squares:
				if square.pos == board_change[1]:
					new_square = square
					new_square_old_piece = new_square.occupying_piece
					new_square.occupying_piece = changing_piece

		pieces = [
			i.occupying_piece for i in self.squares if i.occupying_piece is not None
		]

		if changing_piece is not None:
			if changing_piece.notation == 'K':
				king_pos = new_square.pos
		if king_pos == None:
			for piece in pieces:
				if piece.notation == 'K':
					if piece.color == color:
						king_pos = piece.pos
		for piece in pieces:
			if piece.color != color:
				for square in piece.attacking_squares(self):
					if square.pos == king_pos:
						output = True

		if board_change is not None:
			old_square.occupying_piece = changing_piece
			new_square.occupying_piece = new_square_old_piece
						
		return output


	def is_in_checkmate(self, color):
		output = False

		for piece in [i.occupying_piece for i in self.squares]:
			if piece != None:
				if piece.notation == 'K' and piece.color == color:
					king = piece

		if king.get_valid_moves(self) == []:
			if self.is_in_check(color):
				output = True

		return output


	def get_square_from_pos(self, pos)-> Square:
		for square in self.squares:
			if (square.x, square.y) == (pos[0], pos[1]):
				return square


	def get_piece_from_pos(self, pos):
		return self.get_square_from_pos(pos).occupying_piece


	def draw(self, display, x_offset, y_offset):
		if self.selected_piece is not None:
			self.get_square_from_pos(self.selected_piece.pos).highlight = True
			for square in self.selected_piece.get_valid_moves(self):
				square.highlight = True
			x = self.selected_piece.get_valid_attacks(self)
			for square in x:
				square.attack_highlight = True

		for square in self.squares:
			square.draw(display, x_offset, y_offset )

		