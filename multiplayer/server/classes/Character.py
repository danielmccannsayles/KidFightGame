## Typing Hack - allow imports for type safety w/o causing circular..
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from multiplayer.server.classes.Board import Board

from collections import deque
from multiplayer.server.classes.DefaultPiece import DefaultPiece
import math


class Character(DefaultPiece):
    def __init__(self, pos, color, move_distance, hp, attack_dmg, board: Board):
        self.color = color
        if self.color == "white":
            piece_type = "WC"
        else:
            piece_type = "BC"
        super().__init__(pos, color, piece_type)

        self.move_distance = move_distance
        self.attack_dmg = attack_dmg
        self.max_hp = hp
        self.hp = self.max_hp
        self.board = board

    def to_json(self):
        return {"type": self.piece_type, "hp": self.hp}

    def display_moves(self):
        self.board.clear_highlight()
        moves = self.get_valid_moves()
        self.board.set_highlight(moves)

    def move_towards_closest_opponent(self, opponent_pieces: list[Character]):
        target_character, min_distance = self._find_closest_opponent(opponent_pieces)

        # if min distance is 1 we are already touching
        if min_distance != 1 and target_character:
            self._move_towards(target_character)

    def _find_closest_opponent(self, opponent_pieces: list[Character]):
        """Find the closest opponent piece using Manhattan distance."""
        closest_piece = None
        min_distance = math.inf

        for opponent in opponent_pieces:
            distance = abs(self.row - opponent.row) + abs(self.column - opponent.column)
            if distance < min_distance:
                min_distance = distance
                closest_piece = opponent

        return closest_piece, min_distance

    def _move_towards(self, target: Character):
        """Move whatever valid move is best to go to the target square"""
        if not target:
            return None

        valid_moves = self.get_valid_moves()

        # Calculate the Manhattan distance to the target for each valid move
        best_move = None
        min_distance = math.inf
        for row, column in valid_moves:
            distance = abs(row - target.row) + abs(column - target.column)
            if distance < min_distance:
                min_distance = distance
                best_move = (row, column)

        # Move to the best square, if one is found
        if best_move:
            self.board.move_piece_to_pos(best_move, self)

    def get_valid_moves(self):
        """Returns a list of valid positions the piece can move to based on movement"""
        valid_moves: list[tuple[int, int]] = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # up, right, down, left
        visited = set()
        queue = deque(
            [(self.row, self.column, 0)]
        )  # (current_row, current_col, current_distance)

        while queue:
            current_row, current_col, distance = queue.popleft()

            # Skip if we've already visited this square
            if (current_row, current_col) in visited:
                continue
            visited.add((current_row, current_col))

            # Add the square to valid moves if it's within movement distance
            if distance > 0:  # Exclude the starting square
                valid_moves.append((current_row, current_col))

            # Stop exploring if we've reached the movement limit
            if distance >= self.move_distance:
                continue

            # Explore neighbors
            for dr, dc in directions:
                new_row = current_row + dr
                new_col = current_col + dc

                # Check board bounds
                if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.rows:
                    next_square = (new_row, new_col)

                    # Only move into unoccupied squares
                    if not self.board.check_if_occupied(next_square):
                        queue.append((new_row, new_col, distance + 1))

        return valid_moves
