import pygame

from data.classes.Board import Board

pygame.init()

WINDOW_SIZE = (1000, 1000)
BOARD_SIZE = 800

x_offset = WINDOW_SIZE[0] - BOARD_SIZE
y_offset = WINDOW_SIZE[1] - BOARD_SIZE


screen = pygame.display.set_mode(WINDOW_SIZE)
board = Board(BOARD_SIZE, BOARD_SIZE, x_offset, y_offset)
# menu = Menu(x_offset, WINDOW_SIZE[1])


def draw(display):
    display.fill("white")

    board.draw(display)

    pygame.display.update()


running = True
while running:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        # End
        if event.type == pygame.QUIT:
            running = False

        # Click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # On board
            if (mx >= x_offset) and (my >= y_offset):
                board_x = mx - x_offset
                board_y = my - y_offset
                # Left click
                if event.button == 1:
                    board.handle_click(board_x, board_y)

    # 	if board.is_in_checkmate('black'):
    # 		print('White wins!')
    # 		running = False
    # 	elif board.is_in_checkmate('white'):
    # 		print('Black wins!')
    # 		running = False

    draw(screen)
