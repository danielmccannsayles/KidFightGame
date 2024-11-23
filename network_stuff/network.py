import socket
import pickle
from network_stuff.player import Player


class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.0.0.178"
        self.port = 5555
        self.address = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p

    def connect(self) -> Player:
        try:
            self.client.connect(self.address)
            data = self.client.recv(2048)
            if not data:
                raise ValueError("No data received from the server.")
            return pickle.loads(data)

        except Exception as e:
            print("error connecting: ", e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            data = self.client.recv(2048)
            if not data:
                raise ValueError("No data received from the server.")
            return pickle.loads(data)

        except Exception as e:
            print("error sending: ", e)
