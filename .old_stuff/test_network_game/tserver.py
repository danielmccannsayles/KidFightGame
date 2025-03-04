# Test server

import socket
from _thread import start_new_thread
from network_stuff.player import Player
import pickle

server = "10.0.0.178"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]


def threaded_client(conn: socket.socket, pid):
    initial = pickle.dumps(players[pid])
    print("initializing by sending: ", initial)
    conn.send(initial)
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[pid] = data

            if not data:
                print("Disconnected")
                break
            else:
                if pid == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()


player_id = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, player_id))
    player_id += 1
