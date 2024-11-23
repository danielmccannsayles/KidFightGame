import pygame
from game_stuff.Game import Game


game = Game()

pygame.init()
while game.running:
    game.gameloop()
