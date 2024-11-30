import time
import threading
from llm_stuff.call_gpt import generate_character_stats
from multiplayer.server.classes.Board import Board
from multiplayer.server.classes.Character import Character


class Clock:
    def __init__(self, interval):
        """interval in seconds"""
        self.interval = interval * 1000
        self.last_time = time.time()

    def check(self):
        """Returns true if interval has passed"""
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        if elapsed_time >= self.interval:
            self.last_time = current_time
            return True
        return False


class ServerGame:
    def __init__(self):
        self.clock = Clock(1)

        self.loading_character = False
        self.character_to_add = None

        # Board object for representation.
        self.board = Board()

    def create_character(self, color, description: str):
        "Call gpt to create a character. Currently making a new thread to do so. daemon means it will be terminated"
        if self.loading_character:
            print("Character generation is already in progress.")
            return

        self.loading_character = True
        description = description or "bland default character"

        # Send this back - will self work?
        def post_event(self, response, color):
            self.character_to_add = {"response": response, "color": color}

        # Call API in other thread (not async)
        # TODO: make sure this works now that game is in a threaded context
        threading.Thread(
            target=generate_character_stats,
            args=(self, description, color, post_event),
            daemon=True,
        ).start()

    def add_character_to_game(
        self,
    ):
        """Call after the character is ready to be added"""
        color = self.character_to_add["color"]
        response = self.character_to_add["response"]

        base = self.board.bases[color]
        spawn = base.get_spawn()

        character = Character(
            (0, 0),
            color=color,
            board=self.board,
            attack_dmg=response["AD"],
            hp=response["HP"],
            move_distance=response["MD"],
        )
        self.board.add_character(spawn, character, color)

    def gameloop(self):
        # Do game logic
        if self.clock.check():
            # do piece stuff
            pass

        # Do we need to handle recieving info or sending it here?

        if self.character_to_add:
            self.add_character_to_game()
            self.loading_character = False
