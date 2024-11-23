import pygame
from network_stuff.client import Network
from network_stuff.helpers import make_pos, read_pos

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


class Player:
    def __init__(self, pos: tuple, width, height, color):
        self.x = pos[0]
        self.y = pos[1]

        self.width = width
        self.height = height
        self.color = color
        self.rect = (self.x, self.y, width, height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def redrawWindow(win: pygame.Surface, player: Player, player2: Player):
    win.fill((255, 255, 255))
    player.draw(win)
    player2.draw(win)

    pygame.display.update()


def main():
    run = True
    n = Network()
    start_pos = read_pos(n.getPos())
    print("start pos: ", start_pos)

    color = (0, 255, 0)
    p = Player(start_pos, 100, 100, color)
    p2 = Player((0, 0), 100, 100, color)
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        # Send current position and get opponent position
        p2pos_str = n.send(make_pos((p.x, p.y)))
        p2pos = read_pos(p2pos_str)
        print("p2 pos: ", p2pos)
        p2.x = p2pos[0]
        p2.y = p2pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, p)


main()
