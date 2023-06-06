import socket
import pickle

class Network:
    def __init__(self):
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.tcp_client.settimeout(0)
        self.ip = '127.0.0.1'
        self.port = 10000
        self.address = (self.ip, self.port)

    def n_connect(self):
        try:
            self.tcp_client.connect((self.ip, self.port))
            val = self.tcp_client.recv(8)
            print("Connected")
            return int(val.decode())
        except:
            print("error")
            pass
    def n_disconnect(self):
        self.tcp_client.close()

    def n_send(self, data, pick=False):
        try:
            if pick:
                self.tcp_client.send(pickle.dumps(data))
            else:
                self.tcp_client.send(str.encode(data))
            reply = self.tcp_client.recv(2048)
            try:
                reply = pickle.loads(reply)
            except Exception as e:
                print(e)
            return reply
        except socket.error as e:
            print(e)

start_connect = Network()  # Создание экземпляра класса Network
start_connect.n_connect()  # Вызов метода n_connect для установки подключения к серверу
