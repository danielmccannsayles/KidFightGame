import socket
from _thread import start_new_thread
from helpers import make_pos, read_pos
import random


server = "10.0.0.178"
port = 5555

# socket time
# WE will connect client to the port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# bind server and port to socket - could fail, so need try
try:
    s.bind((server, port))

except socket.error as e:
    print(e)


# open port for (num) clients
s.listen(2)
print("Server started, waiting for connection")

# start_pos = (random.randint(100, 400), random.randint(100, 400))
positions = [(0, 0), (100, 100)]


# Start threading
def threaded_client(conn: socket.socket, pid: int):
    start_pos = make_pos(positions[pid])
    print("Sending starting pos: ", start_pos)
    conn.send(str.encode(start_pos))
    while True:
        try:
            data = read_pos(conn.recv(2048))
            print(data)

            positions[pid] = data

            if not data:
                print(f"{pid}: Disconnected")
                break
            else:
                # Respond with other players data
                if pid == 1:
                    reply = positions[0]
                else:
                    reply = positions[1]

                print(f"{pid}: Recieved: ", data)
                print(f"{pid}: Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))

        except e:
            print(e)
            break

    print("Lost connection")
    conn.close()
    print("Closed connection")


player_id = 0
# Continuously look to accept connections
while True:
    conn, addr = s.accept()  # Waits for connection
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, player_id))
    player_id += 1
