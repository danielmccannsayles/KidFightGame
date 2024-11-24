import pygame

from game_stuff.classes.Menu_Items.Button import Button
from game_stuff.classes.Menu_Items.Clock import Clock, SECOND_TICK_EVENT
from game_stuff.classes.pieces.Character import Character
from game_stuff.classes.Board import Board
from game_stuff.classes.Menu_Items.InputBox import InputBox

from llm_stuff.call_gpt import generate_character_stats
from testing.mock_responses import LARGE_SPIKED_BALL_RESPONSE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Font
pygame.font.init()
FONT = pygame.font.SysFont(None, 36)


class Game:
    def __init__(self) -> None:
        self.WINDOW_SIZE = (1000, 800)
        self.BOARD_SIZE = 700
        self.ROWS = 10

        self.x_offset = self.WINDOW_SIZE[0] - self.BOARD_SIZE
        self.y_offset = self.WINDOW_SIZE[1] - self.BOARD_SIZE

        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        self.board = Board(
            self.BOARD_SIZE, self.BOARD_SIZE, self.x_offset, self.y_offset, self.ROWS
        )
        # menu = Menu(x_offset, WINDOW_SIZE[1])

        # Sprites for buttons - https://stackoverflow.com/questions/47639826/pygame-button-single-click
        # Kinda butchered the code since its fully OOP in the example. Should eventually switch to fully OOP
        self.all_sprites = pygame.sprite.Group()
        clear_button = Button(20, 20, 100, 30, self.reset, "Clear")
        white_button = Button(
            20, 100, 150, 30, lambda: self.add_character("white"), "New White"
        )
        black_button = Button(
            20, 150, 150, 30, lambda: self.add_character("black"), "New Black"
        )
        self.clock = Clock()
        self.all_sprites.add(clear_button, white_button, black_button, self.clock)
        self.input_box = InputBox(20, 200, 140, 32)

        self.character_to_add = None
        self.running = True

    def reset(self):
        self.board.reset_board()

    def add_character(self, color):
        text = self.input_box.text
        self.input_box.clear()

        response = LARGE_SPIKED_BALL_RESPONSE
        # response = generate_character_stats(text)

        print(response)
        # Add w/ default pos - will update later
        self.character_to_add = Character(  # TODO: update this rook to accept an object and initialize from there or sumn
            (0, 0),
            color=color,
            board=self.board,
            attack_dmg=response["AD"],
            hp=response["HP"],
            movespeed=response["MS"],
            rows=self.ROWS,
        )

    def handle_menu_click(self, event):
        for button in self.all_sprites:
            button.handle_event(event)
        self.input_box.handle_event(event)

    def draw(self, display):
        display.fill("white")

        self.board.draw(display)
        self.all_sprites.draw(display)
        self.input_box.draw(display)

        pygame.display.update()

    def gameloop(self):
        self.clock.update()
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == SECOND_TICK_EVENT:
                # TODO: do somethign here
                print("A second has passed!")

            # On board
            if (mx >= self.x_offset) and (my >= self.y_offset):
                board_x = mx - self.x_offset
                board_y = my - self.y_offset
                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Left Click
                    if event.button == 1:
                        if self.character_to_add is not None:
                            self.board.add_character(
                                board_x, board_y, self.character_to_add
                            )
                            self.character_to_add = None
                        else:
                            self.board.handle_click(board_x, board_y)

            # On menu
            else:
                self.handle_menu_click(event)

        self.draw(self.screen)
