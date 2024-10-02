import pygame

from game_stuff.data.classes.Menu_Items.Button import Button
from game_stuff.data.classes.pieces.Rook import Rook
from game_stuff.data.classes.Board import Board


class Game:
        
    pygame.init()

    def __init__(self) -> None:
    
        self.WINDOW_SIZE = (1000, 1000)
        self.BOARD_SIZE = 800

        self.x_offset = self.WINDOW_SIZE[0] - self.BOARD_SIZE
        self.y_offset = self.WINDOW_SIZE[1] - self.BOARD_SIZE

        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        self.board = Board(self.BOARD_SIZE, self.BOARD_SIZE, self.x_offset, self.y_offset, 10)
        # menu = Menu(x_offset, WINDOW_SIZE[1])
        
        # Sprites for buttons - https://stackoverflow.com/questions/47639826/pygame-button-single-click
        # Kinda butchered the code since its fully OOP in the example. Should eventually switch to fully OOP
        self.all_sprites = pygame.sprite.Group()
        clear_button = Button(20, 20, 100, 30, self.resest, "Clear")
        new_button = Button(20, 100, 100, 30, self.add_character, "New")
        self.all_sprites.add(clear_button, new_button)

        self.add_char = False
        self.running = True


    # Button functions
    def resest(self):
        self.board.reset_board()


    
    def add_character(self):
        print("character ready to be added")
        self.add_char = True



    # Handle a click on the menu (not on the board)
    def handle_menu_click(self, event):
        for button in self.all_sprites:
            button.handle_event(event)


    def draw(self, display):
        display.fill("white")

        self.board.draw(display)
        self.all_sprites.draw(display)

        pygame.display.update()


    # TODO: make this a Game class
    def gameloop(self):
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            # End
            if event.type == pygame.QUIT:
                self.running = False

            # On board
            if (mx >= self.x_offset) and (my >=self. y_offset):
                board_x = mx - self.x_offset
                board_y = my - self.y_offset
                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Left Click
                    if event.button == 1:
                        if self.add_char:
                            print
                            self.board.add_character(board_x, board_y)
                            self.add_char = False
                        else:
                            self.board.handle_click(board_x, board_y)

            # Off board
            else:
                self.handle_menu_click(event)

        self.draw(self.screen)
