import time
import threading
from llm_stuff.call_gpt import generate_character_stats_multiplayer
from multiplayer.server.classes.Board import Board
from multiplayer.server.classes.Character import Character


class Clock:
    def __init__(self, interval):
        """Interval in seconds"""
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

        self.loading_character = {"white": False, "black": False}
        self.character_to_add = {"white": None, "black": None}

        # Board object for representation.
        self.board = Board(10)

    def callback(self, response, color):
        """Callback is a method to have access to self"""
        print("callback called")
        self.character_to_add[color] = Character(
            (0, 0),
            color=color,
            board=self.board,
            attack_dmg=response["AD"],
            hp=response["HP"],
            move_distance=response["MD"],
        )

    def create_character(self, color, description: str):
        "Call gpt to create a character. Currently making a new thread to do so. daemon means it will be terminated"
        if self.loading_character[color]:
            print("Character generation is already in progress.")
            return

        self.loading_character[color] = True
        description = description or "bland default character"

        # Call API in other thread (not async)
        # TODO: make sure this works now that game is in a threaded context
        threading.Thread(
            target=generate_character_stats_multiplayer,
            args=(description, color, self.callback),
            daemon=True,
        ).start()

    def add_character_to_game(self, character: Character):
        """Call after the character is ready to be added"""
        print("character exists on game class. Adding it..")
        base = self.board.bases[character.color]
        spawn_pos = base.get_open_spawn_pos()
        self.board.add_piece_safe(spawn_pos, character)
        self.board.characters[character.color].append(character)

    def gameloop(self, color):
        """Runs constantly in while loop"""
        # TODO: how can I only do the game logic for the color that's on board??
        # DUnno yet.. for now just do nothing
        if self.clock.check():
            # do piece stuff
            pass

        # Check if we need to add a character
        character = self.character_to_add[color]
        if character:
            print("game loop: character to add")
            self.add_character_to_game(character)
            self.loading_character[color] = False
            self.character_to_add[color] = None
            print("game loop: finished adding character")

        # Return current board
        return self.board.to_json(), self.loading_character[color]
