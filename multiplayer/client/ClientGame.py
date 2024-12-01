import pygame as pg

from multiplayer.client.game_classes.Board import Board
from multiplayer.client.game_classes.InputBox import InputBox
from multiplayer.client.network import Network


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

        self.character_description = None
        self.loading = False

        # Start the network and get the starting board
        self.n = Network()
        self.update_local(self.n.get_start())
        self.draw()

    def request_new_character(self, description):
        """Called on enter of input box"""
        if self.loading:
            print(f"still loading..")
            return

        print(f"new char requested w/ {description}")
        self.character_description = description

    def update_local(self, recieve_obj):
        """Update local values"""
        board_list = recieve_obj["board"]
        loading = recieve_obj["loading"]
        self.board.update_board(board_list)

        # TODO: gray out the button?
        self.loading = loading

    def draw(self):
        self.screen.fill("white")
        self.board.draw(self.screen)
        self.input_box.draw(self.screen)
        pg.display.update()

    def gameloop(self):
        # Cap refresh rate
        self.clock.tick(60)

        # If we have something to send, add it to send_obj
        send_obj = {}
        if self.character_description:
            send_obj["description"] = self.character_description
            self.character_description = None

        # Get from server
        recieve_obj = self.n.send(send_obj)
        self.update_local(recieve_obj)

        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            else:
                self.input_box.handle_event(event)

        self.draw()
