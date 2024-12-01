import socket
import json
from server_address import SERVER_ADDRESS


class Network:
    """Handles all the client side networking"""

    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER_ADDRESS
        self.port = 5555
        self.address = (self.server, self.port)
        self.start = self.connect()

    def get_start(self):
        return self.start

    def connect(self):
        """Connect for the first time. Returns a board list"""
        try:
            self.client.connect(self.address)
            data = self.client.recv(2048).decode()
            if not data:
                raise ValueError("No data received from the server.")
            return json.loads(data)

        except Exception as e:
            print("error connecting: ", e)

    def send(self, data: dict):
        """Send a json object every tick. Returns a dict with 'board' and 'loading'"""
        try:
            json_data = json.dumps(data).encode()
            self.client.send(json_data)
            data = self.client.recv(2048).decode()
            if not data:
                raise ValueError("No data received from the server.")
            return json.loads(data)

        except Exception as e:
            print("error sending: ", e)
