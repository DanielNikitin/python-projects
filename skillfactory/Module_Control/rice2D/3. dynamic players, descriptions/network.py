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

    def getP(self):  # подключаем персонажа к серверу и возвращаем данные об персонаже
        return self.p

    def connect(self):  #  устанавливает соединение с сервером и возвращает начальное состояние игрока.
        try:

            self.client.connect(self.addr)  # подключаемся к серверу
            return pickle.loads(self.client.recv(2048))  # получаем данные от сервера

        except:
            self.client.close()

    def send(self, data):  # отправляет данные о состоянии игрока серверу и получает обновленные данные о состоянии других игроков.
        try:

            print(f"Sending to server :: {data}")
            self.client.send(pickle.dumps(data))

            reply = pickle.loads(self.client.recv(2048))
            print(f"Received from server :: {reply}")
            return reply

        except socket.error as e:
            print(e)