import pygame
import threading

from game_stuff.classes.Menu_Items.Button import Button
from game_stuff.classes.Menu_Items.ClockWrapper import ClockWrapper
from game_stuff.classes.pieces.Character import Character
from game_stuff.classes.Board import Board
from game_stuff.classes.Menu_Items.InputBox import InputBox
from game_stuff.events import SECOND_TICK_EVENT, CHARACTER_RESPONSE_EVENT

from llm_stuff.call_gpt import generate_character_stats

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
        self.BOARD_SIZE = 800
        self.ROWS = 10

        self.x_offset = self.WINDOW_SIZE[0] - self.BOARD_SIZE
        self.y_offset = self.WINDOW_SIZE[1] - self.BOARD_SIZE

        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        self.board = Board(self.BOARD_SIZE, self.x_offset, self.y_offset, self.ROWS)
        # menu = Menu(x_offset, WINDOW_SIZE[1])

        # Sprites for buttons - https://stackoverflow.com/questions/47639826/pygame-button-single-click
        # Kinda butchered the code since its fully OOP in the example. Should eventually switch to fully OOP
        self.all_sprites = pygame.sprite.Group()
        clear_button = Button(20, 20, 100, 30, self.reset, "Clear")
        white_button = Button(
            20, 100, 150, 30, lambda: self.create_character("white"), "New White"
        )
        black_button = Button(
            20, 150, 150, 30, lambda: self.create_character("black"), "New Black"
        )
        self.clock_wrapper = ClockWrapper((20, 20))
        self.all_sprites.add(
            clear_button, white_button, black_button, self.clock_wrapper
        )
        self.loading_character = False

        # Enable key repeat (delay: 400ms, interval: 50ms) - do this so the input box keys can be held down
        pygame.key.set_repeat(400, 50)
        self.input_box = InputBox(20, 200, 140, 32)

        self.character_to_add = None
        self.running = True

    def reset(self):
        self.board.reset_board()

    def create_character(self, color):
        if self.loading_character:
            print("Character generation is already in progress.")
            return

        self.loading_character = True
        description = self.input_box.text or "bland default character"
        self.input_box.clear()

        # Send event back - will be listened to in game loop
        def post_event(response, color):
            pygame.event.post(
                pygame.event.Event(
                    CHARACTER_RESPONSE_EVENT, {"response": response, "color": color}
                )
            )

        # Call API in other thread (not async)
        threading.Thread(
            target=generate_character_stats,
            args=(description, color, post_event),
            daemon=True,
        ).start()

    # Add a character once its generated
    def add_character_to_game(self, event_dict):
        color = event_dict["color"]
        response = event_dict["response"]
        base = self.board.bases[color]
        spawn = base.get_spawn()
        character = Character(  # TODO: update this to accept an object and initialize from there or sumn
            (0, 0),
            color=color,
            board=self.board,
            attack_dmg=response["AD"],
            hp=response["HP"],
            movespeed=response["MS"],
        )
        self.board.add_character(spawn, character)

    def handle_menu_click(self, event):
        for button in self.all_sprites:
            button.handle_event(event)

    def draw(self, display):
        display.fill("white")

        self.board.draw(display)
        self.all_sprites.draw(display)
        self.input_box.draw(display)

        pygame.display.update()

    def gameloop(self):
        self.clock_wrapper.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == SECOND_TICK_EVENT:
                # TODO: do somethign here
                # print("A second has passed!")
                pass

            elif event.type == CHARACTER_RESPONSE_EVENT:
                self.add_character_to_game(event.dict)
                self.loading_character = False

            # General events
            else:
                self.input_box.handle_event(event)
                self.handle_menu_click(event)

        self.draw(self.screen)


# Deprecated click on board code
# On board
# mx, my = pygame.mouse.get_pos()
# elif (mx >= self.x_offset) and (my >= self.y_offset):
#     board_x = mx - self.x_offset
#     board_y = my - self.y_offset
#     # Click
#     if event.type == pygame.MOUSEBUTTONDOWN:
#         # Left Click
#         if event.button == 1:
#             if self.character_to_add is not None:
#                 self.board.add_character(
#                     board_x, board_y, self.character_to_add
#                 )
#                 self.character_to_add = None
#             else:
#                 self.board.handle_click(board_x, board_y)
