import pygame

from data.classes.Board import Board
from data.classes.Menu_Items.Button import Button
from data.classes.pieces.Rook import Rook

pygame.init()

WINDOW_SIZE = (1000, 1000)
BOARD_SIZE = 800

x_offset = WINDOW_SIZE[0] - BOARD_SIZE
y_offset = WINDOW_SIZE[1] - BOARD_SIZE

screen = pygame.display.set_mode(WINDOW_SIZE)
board = Board(BOARD_SIZE, BOARD_SIZE, x_offset, y_offset, 10)
# menu = Menu(x_offset, WINDOW_SIZE[1])


# Button functions
def resest():
    board.reset_board()


add_char = False  # On when adding a new character and picking a spot
def add_character():
    print("character ready to be added")
    global add_char 
    add_char = True


# Sprites for buttons - https://stackoverflow.com/questions/47639826/pygame-button-single-click
# Kinda butchered the code since its fully OOP in the example. Should eventually switch to fully OOP
all_sprites = pygame.sprite.Group()
clear_button = Button(20, 20, 100, 30, resest, "Clear")
new_button = Button(20, 100, 100, 30, add_character, "New")
all_sprites.add(clear_button, new_button)


# Handle a click on the menu (not on the board)
def handle_menu_click(event):
    for button in all_sprites:
        button.handle_event(event)


def draw(display):
    display.fill("white")

    board.draw(display)
    all_sprites.draw(display)

    pygame.display.update()


# TODO: make this a Game class

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
                    if add_char:
                        print
                        board.add_character(board_x, board_y)
                        add_char = False
                    else:
                        board.handle_click(board_x, board_y)

        # Off board
        else:
            handle_menu_click(event)

    draw(screen)
