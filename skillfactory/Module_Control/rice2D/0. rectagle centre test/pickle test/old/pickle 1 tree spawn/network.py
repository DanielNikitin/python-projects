import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 10000
        self.addr = (self.server, self.port)
        self.server_bridge = self.connect()
        print(f"Server Connect Status :: {self.server_bridge}")


    def get_data(self):  # получаем дату от сервера
        return self.server_bridge  # через функцию connect


#   ----------- CONNECT / SEND -----------
    def connect(self):  #  устанавливает соединение с сервером
        try:
            self.client.connect(self.addr)  # подключаемся к серверу
            return pickle.loads(self.client.recv(2048)) # получаем данные клиента
        except:
            self.client.close()
            print("** SERVER IS SHUTTED DOWN **")

#   -------- Отправка и Получение Ответа
    def send_and_rec(self, rec_data):
        try:
            print(f"Sending to server :: {rec_data}")
            self.client.send(pickle.dumps(rec_data))

            reply = pickle.loads(self.client.recv(2048))
            print(f"Received from server :: {load_data}")
            return reply  # отправляем то что получилось после ответа
        except socket.error as e:
            print(e)

#   -------- Только Отправка Даты
    def send(self, rec_data):
        try:
            print(f"Sending to server :: {rec_data}")
            # pickle dumps преобразовать в байты для отправки
            self.client.send(pickle.dumps(rec_data))
            return  # Убираем попытку получения ответа
        except socket.error as e:
            print(e)
#   --------------------------------------

#n=Network()
#print(n.send({'message': 'pickle_base_server_client_network message from def send'}))
#print(n.send_and_rec({'message': 'pickle_base_server_client_network message from def send_and_rec'}))