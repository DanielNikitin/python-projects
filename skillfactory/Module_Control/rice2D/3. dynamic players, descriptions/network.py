import socket
import pickle

from player import Player

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 10000
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)  # подключаемся к серверу
            return pickle.loads(self.client.recv(2048))  # получаем данные от сервера
        except:
            self.client.close()
            return Player(0, 0, 0, 0, (0, 0, 0), None)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))

            reply = pickle.loads(self.client.recv(2048))
            return reply

        except socket.error as e:
            print(e)
