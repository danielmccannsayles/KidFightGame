import pygame as pg
from network_stuff.client import Network
from network_stuff.player import Player


width = 500
height = 500
win = pg.display.set_mode((width, height))
pg.display.set_caption("Client")


def redrawWindow(win: pg.Surface, player: Player, player2: Player):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)
    pg.display.update()


def main():
    run = True
    n = Network()
    p1 = n.get_p()
    clock = pg.time.Clock()

    while run:
        clock.tick(60)
        p2 = n.send(p1)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

        p1.move()
        redrawWindow(win, p1, p2)


main()
