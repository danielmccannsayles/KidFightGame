import socket
from _thread import start_new_thread
from helpers import make_pos, read_pos


server = "10.0.0.178"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


positions = [(0, 0), (100, 100)]


def threaded_client(conn, pid: int):
    conn.send(str.encode(make_pos(positions[pid])))
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            positions[pid] = data

            if not data:
                print("Disconnected")
                break
            else:
                if pid == 1:
                    reply = positions[0]
                else:
                    reply = positions[1]

                print(f"{pid} Received: ", data)
                print(f"{pid} Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()


player_id = 0
while True:
    conn, addr = s.accept()
    print(f"Player {player_id} joined at:", addr)

    start_new_thread(threaded_client, (conn, player_id))
    player_id += 1
