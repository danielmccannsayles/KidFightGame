# IT's server time baby!!


# we want our server to ... make a new thread and send a board object back when it connects

# For now I'm not going to code any logic. Just send back a random board.
# Test server

import socket
from _thread import start_new_thread
from multiplayer.client.helpers import get_mock_board
import json
import time


server = "10.0.0.178"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

MOCK_BOARD1 = get_mock_board()
MOCK_BOARD2 = get_mock_board()


def threaded_client(conn: socket.socket):
    initial = json.dumps(MOCK_BOARD1).encode()
    conn.send(initial)

    # TODO: move timer to a class when its more widely used
    # Setup timer
    interval = 5  # Trigger every 5 seconds
    last_trigger_time = time.time()
    mock1 = True

    reply = ""
    while True:
        # TODO: we need to run a game loop here

        # Every 5 seconds flip the one we send
        current_time = time.time()
        if current_time - last_trigger_time >= interval:
            mock1 = not mock1
            last_trigger_time = current_time  # Update the last trigger time

        try:
            data = conn.recv(2048).decode()
            if not data:
                print("Disconnected")
                break
            else:
                reply = MOCK_BOARD1 if mock1 else MOCK_BOARD2
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(json.dumps(reply).encode())
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))
