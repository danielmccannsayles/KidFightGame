import pygame as pg
from multiplayer.client.ClientGame import ClientGame


pg.init()


def main():
    game = ClientGame()

    while True:
        game.gameloop()


main()
