import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 10000
        self.addr = (self.server, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)  # подключаемся к серверу
            print("Connected to Server")
            return pickle.loads(self.client.recv(2048))  # получаем данные от сервера
        except:
            print("Server is Shutted Down")
            self.client.close()

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            reply = pickle.loads(self.client.recv(2048))
            return reply
        except socket.error as e:
            print(e)

    def disconnect(self):
        self.client.close()
        print("disconnected")