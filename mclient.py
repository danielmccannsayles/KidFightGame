from multiplayer.ClientGame import ClientGame


def main():
    game = ClientGame()

    while True:
        game.gameloop()


main()
