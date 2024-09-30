import pygame

from data.classes.Board import Board
from data.classes.Menu_Items.Button import Button

pygame.init()

WINDOW_SIZE = (1000, 1000)
BOARD_SIZE = 800

x_offset = WINDOW_SIZE[0] - BOARD_SIZE
y_offset = WINDOW_SIZE[1] - BOARD_SIZE

screen = pygame.display.set_mode(WINDOW_SIZE)
board = Board(BOARD_SIZE, BOARD_SIZE, x_offset, y_offset)
# menu = Menu(x_offset, WINDOW_SIZE[1])


# Button functions
def start():
    print("starting")


def quit():
    print("quitting")


# Sprites for buttons - https://stackoverflow.com/questions/47639826/pygame-button-single-click
# Kinda butchered the code since its fully OOP. Should eventyually switch to this
all_sprites = pygame.sprite.Group()
start_button = Button(20, 20, 50, 30, start, "Start")
quit_button = Button(20, 100, 50, 30, quit, "Quit")
all_sprites.add(start_button, quit_button)


# Handle a click on the menu (not on the board)
def handle_menu_click(event):
    for button in all_sprites:
        button.handle_event(event)


def draw(display):
    display.fill("white")

    board.draw(display)
    all_sprites.draw(display)

    pygame.display.update()


running = True
while running:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        # End
        if event.type == pygame.QUIT:
            running = False

        # On board
        if (mx >= x_offset) and (my >= y_offset):
            board_x = mx - x_offset
            board_y = my - y_offset
            # Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left Click
                if event.button == 1:
                    board.handle_click(board_x, board_y)

        # Off board
        else:
            handle_menu_click(event)

    # 	if board.is_in_checkmate('black'):
    # 		print('White wins!')
    # 		running = False
    # 	elif board.is_in_checkmate('white'):
    # 		print('Black wins!')
    # 		running = False

    draw(screen)
