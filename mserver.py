# IT's server time baby!!


# we want our server to ... make a new thread and send a board object back when it connects

# For now I'm not going to code any logic. Just send back a random board.
# Test server

import socket
from _thread import start_new_thread
from multiplayer.client.helpers import get_mock_board
import json
import time
from multiplayer.server.ServerGame import ServerGame


server = "10.0.0.178"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

server_game = ServerGame()

# TODO: move this to the server game
players = {"black": False, "white": False}


def threaded_client(conn: socket.socket, color: str):
    """
    Protocol:
    data: {}
    """
    initial = json.dumps(
        {"loading": False, "board": server_game.board.to_json()}
    ).encode()
    conn.send(initial)

    while True:
        try:
            data = conn.recv(2048).decode()
            if not data:
                print("Disconnected")
                break

            json_data = json.loads(data)

            # If we get data saying we want a new character
            if "description" in json_data:
                server_game.create_character(color, json_data["description"])
                print("recieved description ", json_data["description"])

            # Call this every iteration. handles game logic & and other stuff
            board_json, loading = server_game.gameloop(color)

            # print("Received: ", data)
            # print("Sending : ", board_json)

            conn.sendall(json.dumps({"loading": loading, "board": board_json}).encode())
        except Exception as e:
            print("threaded client: ", e)
            break

    print("Lost connection to ", color)
    players[color] = False
    conn.close()


""" Main loop. Handle new connections"""
while True:
    # TODO: refactor this logic..
    p1 = players["black"]
    p2 = players["white"]

    conn, addr = s.accept()

    if not p1:
        print("Black player:", addr)
        start_new_thread(threaded_client, (conn, "black"))
        players["black"] = True
    elif not p2:
        print("White player:", addr)
        start_new_thread(threaded_client, (conn, "white"))
        players["white"] = True
    else:
        print("All players connected")
