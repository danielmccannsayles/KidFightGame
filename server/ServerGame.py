import time
import threading
from llm.call_gpt import generate_character_stats_multiplayer
from server.classes.Board import Board
from server.classes.Character import Character


class Clock:
    def __init__(self, interval, stopped=False):
        """Interval in seconds"""
        self.interval = interval
        self.last_time = time.time()
        self.stopped = stopped

    def check(self):
        """Returns true if interval has passed"""
        if self.stopped:
            return False
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        # print(f"Current: {current_time}, Last: {self.last_time}")
        if elapsed_time >= self.interval:
            self.last_time = current_time
            return True
        return False

    def stop(self):
        """Stop timer completely. Does not record elapsed time."""
        self.stopped = True

    def restart(self):
        """Restart timer. Start from 0 seconds"""
        self.last_time = time.time()
        self.stopped = False


class ServerGame:
    def __init__(self):
        self.main_clock = Clock(1)
        self.sub_clock = Clock(1, stopped=True)

        self.loading_character = {"white": False, "black": False}
        self.character_to_add = {"white": None, "black": None}
        self.turn = "white"
        self.opponent = "black"

        # Board object for representation.
        self.board = Board(10)

        # TODO: come up with a more elegant solution - maybe run main loop in other thread
        # Lock prevents main check from running twice (called in two threads)
        self.lock = threading.Lock()

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

    def move_character(self):
        """Take the first character of characters to process and move it"""
        character = next(self.characters_to_process, None)
        if character:
            character.display_moves()
            opponent_characters = self.board.characters[self.opponent]
            character.move_towards_closest_opponent(opponent_characters)

    def gameloop(self, color):
        """Runs constantly in while loop"""
        if self.main_clock.check():
            print("every second")
            # Stop current clock
            self.sub_clock.stop()
            self.board.clear_highlight()

            # Alternate turns every second
            # TODO: fix clunky logic
            if self.turn == "white":
                self.turn = "black"
                self.opponent = "white"
            else:
                self.turn = "white"
                self.opponent = "black"

            print("alternating turn: ", self.turn)

            characters = self.board.characters[self.turn]
            num_c = len(characters)

            if num_c > 0:
                self.characters_to_process = iter(characters)

                # Move once (important b.c. set timer will wait 1 interval)
                self.move_character()
                # round to 4 decimal places
                # dunno if -.02 is necessary but want to make sure it never overlaps
                interval = round((1 - 0.02) / num_c, 4)
                self.sub_clock = Clock(interval)

        if self.sub_clock.check():
            self.move_character()

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
