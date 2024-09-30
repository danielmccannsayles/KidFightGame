import pygame

from data.classes.Board import Board

pygame.init()

WINDOW_SIZE = (1000, 1000)
BOARD_SIZE = 800
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(BOARD_SIZE, BOARD_SIZE)

x_offset = WINDOW_SIZE[0] - BOARD_SIZE
y_offset = WINDOW_SIZE[1] - BOARD_SIZE

def draw(display):
	display.fill('white')

	board.draw(display, x_offset, y_offset)

	pygame.display.update()


running = True
while running:
	mx, my = pygame.mouse.get_pos()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				
				board.handle_click(mx, my,  x_offset, y_offset)


#	if board.is_in_checkmate('black'):
#		print('White wins!')
#		running = False
#	elif board.is_in_checkmate('white'):
#		print('Black wins!')
#		running = False

	draw(screen)