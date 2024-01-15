import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 10000
        self.addr = (self.server, self.port)

        self.server_connect = self.connect()
        if self.connect is not None:
            print("CLIENT :: Connected Successfully")
        print(f"Server Data :: {self.server_connect}")

    def get_server_data(self):  # используется за счет def connect()
        return self.server_connect

    def connect(self):
        try:
            self.client.connect(self.addr)  # подключаемся к серверу
            return pickle.loads(self.client.recv(2048))  # получаем данные от сервера
        except:
            self.client.close()
            print("** SERVER IS SHUTTED DOWN **")

    def send_get_data(self, received_data):
        try:
<<<<<<< Updated upstream

            print(f"NETWORK :: "
                  f"Sending to Server :: {received_data}\n")
            self.client.send(pickle.dumps(received_data))  # отправляем байты

            updated_data = pickle.loads(self.client.recv(2048))
            return updated_data

=======
            self.client.send(pickle.dumps(received_data))  # отправляем байты

            received_data = (self.client.recv(2048))  # получили байты
            pickle.loads(received_data)  # получаем данные
            return received_data
>>>>>>> Stashed changes
        except socket.error as e:
            print(e)
