import pygame

class Square:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.abs_x = x * width
		self.abs_y = y * height
		self.abs_pos = (self.abs_x, self.abs_y)
		self.pos = (x, y)
		self.color = 'light' if (x + y) % 2 == 0 else 'dark'
		self.draw_color = (241, 211, 170) if self.color == 'light' else (180, 126, 82)
		self.highlight_color = (150, 255, 100) if self.color == 'light' else (50, 220, 0)
		self.occupying_piece = None
		self.coord = self.get_coord()
		self.highlight = False
		self.attack_highlight = False
		self.number_font  = pygame.font.SysFont( None, 16 )
		self.hp_color = (220,20,60)
	




	def get_coord(self):
		columns = 'abcdefgh'
		return columns[self.x] + str(self.y + 1)


	def draw(self, display, x_offset, y_offset):
		self.rect = pygame.Rect(
			self.abs_x + x_offset,
			self.abs_y + y_offset,
			self.width,
			self.height
		)
		self.hp_rect = pygame.Rect(
			self.abs_x + x_offset,
			self.abs_y + y_offset,
			self.width,
			10
		)
		
		if self.highlight:
			pygame.draw.rect(display, self.highlight_color, self.rect)
		elif self.attack_highlight:
			pygame.draw.rect(display, self.hp_color, self.rect)
		else:
			pygame.draw.rect(display, self.draw_color, self.rect)

		if self.occupying_piece != None:
			centering_rect = self.occupying_piece.img.get_rect()
			centering_rect.center = self.rect.center
			display.blit(self.occupying_piece.img, centering_rect.topleft)
			pygame.draw.rect(display, self.hp_color, self.hp_rect)
			hptext = str(self.occupying_piece.hp)
			number_image = self.number_font.render( hptext, True, (10,10,10), (255,255,255) )
			display.blit(number_image, centering_rect.topleft)



