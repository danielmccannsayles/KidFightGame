import pygame as pg
from client.ClientGame import ClientGame


pg.init()


def main():
    game = ClientGame()
    while True:
        game.gameloop()


main()
