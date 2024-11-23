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
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, player: Player):
        try:
            self.client.send(pickle.dumps(player))
            return pickle.loads(self.client.recv(2048))  # Pickle is empty here
        except socket.error as e:
            print(e)
