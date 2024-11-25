import socket
import pickle
import json


class Network:
    """Handles all the client side networking"""

    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.0.0.178"
        self.port = 5555
        self.address = (self.server, self.port)
        self.start = self.connect()

    def get_start(self):
        return self.start

    def connect(self):
        """Connect for the first time. Returns a board object"""
        try:
            self.client.connect(self.address)
            data = self.client.recv(1024).decode()
            if not data:
                raise ValueError("No data received from the server.")
            return pickle.loads(data)

        except Exception as e:
            print("error connecting: ", e)

    def send(self, data):
        """Send every tick. Returns an updated board dict"""
        try:
            self.client.send("get".encode())
            data = self.client.recv(1024).decode()
            if not data:
                raise ValueError("No data received from the server.")
            return json.loads(data)

        except Exception as e:
            print("error sending: ", e)
