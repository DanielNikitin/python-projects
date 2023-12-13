import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 10000
        self.addr = (self.server, self.port)

        self.server_connect = self.connect()
        print(f"Server Data :: {self.server_connect}")

    def get_server_data(self):  # используется за счет def connect()
        return self.server_connect

    def connect(self):
        try:
            self.client.connect(self.addr)
            received_data = (self.client.recv(2048))  # получили байты
            return pickle.loads(received_data)  # изменение формата в нормальный
        except:
            self.client.close()
            print("** SERVER IS SHUTTED DOWN **")

    def send_data(self, received_data):
        try:
            print(f"NETWORK: "
                  f"Sending to Server :: {received_data}\n")
            self.client.send(pickle.dumps(received_data))  # отправляем байты
        except socket.error as e:
            print(e)
