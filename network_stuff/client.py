import socket


class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.0.0.178"
        self.port = 5555
        self.address = (self.server, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data: str):
        print(f"n.sned {data}")
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()

        except socket.error as e:
            print(e)
