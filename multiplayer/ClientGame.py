import pygame as pg

from multiplayer.Board import Board
from multiplayer.InputBox import InputBox
import pygame as pg
from multiplayer.network import Network
from multiplayer.Board import Board

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Font
pg.font.init()
FONT = pg.font.SysFont(None, 36)


class ClientGame:
    def __init__(self):
        self.WINDOW_SIZE = (1000, 800)
        self.BOARD_SIZE = 800
        self.ROWS = 10
        self.x_offset = self.WINDOW_SIZE[0] - self.BOARD_SIZE
        self.y_offset = self.WINDOW_SIZE[1] - self.BOARD_SIZE

        self.screen = pg.display.set_mode(self.WINDOW_SIZE)
        pg.display.set_caption("Kid Fight Game")

        self.board = Board(self.BOARD_SIZE, self.x_offset, self.y_offset, self.ROWS)
        self.input_box = InputBox(20, 200, 140, 32, self.request_new_character)
        self.clock = pg.time.Clock()

        # Enable key repeat (delay: 400ms, interval: 50ms) - do this so the input box keys can be held down
        pg.key.set_repeat(400, 50)

        # Start the network and get the starting board
        self.n = Network()
        self.update_local(self.n.get_start())
        self.draw()

    def request_new_character(description):
        """Called on enter of input box"""
        print(f"new char requested w/ {description}")

    def update_local(self, board: Board):
        """Update the local board, squares, characters, etc."""
        self.board = board

    def draw(self):
        self.screen.fill("white")
        self.board.draw(self.screen)
        self.input_box.draw(self.screen)
        pg.display.update()

    def gameloop(self):
        # Cap refresh rate
        self.clock.tick(60)

        # Get updated board
        board_json = self.n.send("get")
        board = Board.update_board(board_json)
        self.update_local(board)

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            else:
                self.input_box.handle_event(event)

        self.draw(self.screen)
