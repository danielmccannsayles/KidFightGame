## Typing Hack - allow imports for type safety w/o causing circular..
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_stuff.classes.Board import Board
    from game_stuff.classes.Square import Square

import pygame
from collections import deque
from game_stuff.classes.pieces.DefaultPiece import DefaultPiece
import math
import os

# Needed for relative import when developing (mac v. windows paths)
current_dir = os.path.dirname(__file__)


# This is the main character piece
class Character(DefaultPiece):
    def __init__(self, pos, color, board: Board, move_distance, hp, attack_dmg):
        if (color) == "white":
            img_path = f"{current_dir}/../../imgs/brutal-helm.png"
        else:
            img_path = f"{current_dir}/../../imgs/orc-head.png"

        img = pygame.image.load(img_path)
        img = pygame.transform.scale(
            img, (board.square_size - 20, board.square_size - 20)
        )

        # DO this down here to init img
        super().__init__(pos, color, img)

        self.move_distance = move_distance
        self.max_hp = hp
        self.hp = self.max_hp

        self.attack_dmg = attack_dmg
        self.board = board

    def display_moves(self):
        self.board.clear_highlight()
        moves = self.get_valid_moves()
        for square in moves:
            square.highlight = True

    def move_towards_closest_opponent(self, opponent_pieces: list[Character]):
        target_character, min_distance = self._find_closest_opponent(opponent_pieces)

        # if min distance is 1 we are already touching
        if min_distance != 1 and target_character:
            # print(f"target found: {target_character.row, target_character.column}")
            self._move_towards(target_character)

    def _find_closest_opponent(self, opponent_pieces: list[Character]):
        """Find the closest opponent piece using Manhattan distance."""
        # print(opponent_pieces)
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
            return None  # No target provided

        # Get valid moves for the piece
        valid_moves = self.get_valid_moves()

        # Calculate the Manhattan distance to the target for each valid move
        best_move = None
        min_distance = math.inf
        for square in valid_moves:
            distance = abs(square.row - target.row) + abs(square.column - target.column)
            if distance < min_distance:
                min_distance = distance
                best_move = square

        # Move to the best square, if one is found
        if best_move:
            prev_square = self.board.get_square_from_board_pos(self.pos)
            prev_square.occupying_piece = None

            self.set_pos(best_move.get_pos())
            best_move.occupying_piece = self
            self.has_moved = True

    def get_valid_moves(self):
        """Returns a list of valid squares the piece can move to based on movement"""
        valid_moves: list[Square] = []
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
                valid_moves.append(
                    self.board.get_square_from_board_pos((current_row, current_col))
                )

            # Stop exploring if we've reached the movement limit
            if distance >= self.move_distance:
                continue

            # Explore neighbors
            for dr, dc in directions:
                new_row = current_row + dr
                new_col = current_col + dc

                # Check board bounds
                if 0 <= new_row < self.board.rows and 0 <= new_col < self.board.rows:
                    next_square = self.board.get_square_from_board_pos(
                        (new_row, new_col)
                    )
                    # Only move into unoccupied squares
                    if next_square.occupying_piece is None:
                        queue.append((new_row, new_col, distance + 1))

        return valid_moves

    # def get_possible_moves(self):
    #     output = []

    #     # What is this??
    #     vertical_range = range(
    #         self.row - self.movespeed, self.column + self.movespeed + 1
    #     )
    #     horizontal_range = range(
    #         self.column - self.movespeed, self.row + self.movespeed + 1
    #     )

    #     # What is hapening? I think we are checking that we can move.. should move this to board
    #     moves_vertical = []
    #     for t in vertical_range:
    #         if (t >= 0) and (t < self.board.rows) and not (t == self.column):
    #             moves_vertical.append(
    #                 self.board.get_square_from_board_pos((self.row, t))
    #             )
    #     output.append(moves_vertical)

    #     # Same.. think we are
    #     moves_horizontal = []
    #     for t in horizontal_range:
    #         if (t >= 0) and (t < self.board.rows) and not (t == self.row):
    #             moves_horizontal.append(
    #                 self.board.get_square_from_board_pos((t, self.column))
    #             )
    #     output.append(moves_horizontal)
    #     return output
