import pygame

class Piece:
	def __init__(self, pos, color, board):
		self.pos = pos
		self.x = pos[0]
		self.y = pos[1]
		self.color = color
		self.has_moved = False

	def move(self, board, square, force=False):

		for i in board.squares:
			i.highlight = False
			i.attack_highlight = False

		if square in self.get_valid_moves(board) or force:
			prev_square = board.get_square_from_pos(self.pos)
			self.pos, self.x, self.y = square.pos, square.x, square.y

			prev_square.occupying_piece = None
			square.occupying_piece = self
			board.selected_piece = None
			self.has_moved = True

			return True
		elif square in self.get_valid_attacks(board):
			square.occupying_piece.hp = square.occupying_piece.hp - self.attack_dmg
			if(square.occupying_piece.hp <= 0):
				prev_square = board.get_square_from_pos(self.pos)
				self.pos, self.x, self.y = square.pos, square.x, square.y

				prev_square.occupying_piece = None
				square.occupying_piece = self
				self.has_moved = True

			# Moved this to prevent multi-attack. Should refactor selected & turn state
			board.selected_piece = None
			return True		
		else:
			board.selected_piece = None
			return False


	def get_moves(self, board):
		output = []
		for direction in self.get_possible_moves(board):
			for square in direction:
				if square.occupying_piece is None:
					output.append(square)

		return output

	def get_valid_attacks(self, board):
		output = []
		for direction in self.get_possible_moves(board):
			for square in direction:
				if square.occupying_piece is not None:
					if square.occupying_piece.color != self.color:
						output.append(square)
		
		return output


	def get_valid_moves(self, board):
		output = []
		for square in self.get_moves(board):
			if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
				output.append(square)

		return output


	# True for all pieces except pawn
	def attacking_squares(self, board):
		return self.get_moves(board)