import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 10000
        self.addr = (self.server, self.port)
        self.server_conn_status = self.connect()
        print(f"Server Connect Status :: {self.server_conn_status}")


    def get_data(self):  # получаем дату от сервера
        return self.server_conn_status


#   ----------- CONNECT / SEND -----------
    def connect(self):
        try:
            self.client.connect(self.addr)
            return True  # If connection is successful
        except socket.error as e:
            print(f"Failed to connect to the server: {e}")
            self.client.close()
            return False  # If connection fails

#   -------- Отправка и Получение Ответа
    def send_and_rec(self, rec_data):
        try:
            print(f"Sending to server :: {rec_data}")
            self.client.send(pickle.dumps(rec_data))  # отправляем байты

            load_data = pickle.loads(self.client.recv(2048))  # переведенная дата в нормальный вид
            print(f"Received from server :: {load_data}")
            return load_data  # отправляем то что получилось после ответа
        except socket.error as e:
            print(e)

#   -------- Только Отправка Даты
    def send(self, rec_data):
        try:
            print(f"Sending to server :: {rec_data}")
            self.client.send(pickle.dumps(rec_data))  # отправляем байты
            return  # Убираем попытку получения ответа
        except socket.error as e:
            print(e)
#   --------------------------------------

#n=Network()
#print(n.send({'message': 'test message from def send'}))
#print(n.send_and_rec({'message': 'test message from def send_and_rec'}))