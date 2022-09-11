import socket
import pickle

from back.log_service import add_log_warnning


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            a = self.client.recv(2048).decode()
            return a
        except:
            add_log_warnning("Network, connect: did not succeed to connect")
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            add_log_warnning("Network: send, socket.error (" + str(e) + ")")
