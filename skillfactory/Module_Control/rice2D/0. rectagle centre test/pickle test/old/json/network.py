import socket
import json


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 10000
        self.addr = (self.server, self.port)
        self.server_con_status = self.connect()
        print(f"Server Connect Status :: {self.server_con_status}")


    def get_data(self):  # получаем дату от сервера
        return self.server_con_status  # через функцию connect


#   ----------- CONNECT / SEND -----------
    def connect(self):  #  устанавливает соединение с сервером
        try:
            self.client.connect(self.addr)  # подключаемся к серверу
            return json.loads(self.client.recv(2048).decode('utf-8'))  # получаем данные клиента
        except:
            self.client.close()
            print("** SERVER IS SHUTTED DOWN **")

#   -------- Отправка и Получение Ответа
    def send_and_rec(self, data):
        try:
            print(f"Sending to server :: {data}")
            self.client.send(json.dumps(data).encode('utf-8'))

            reply = json.loads(self.client.recv(2048).decode('utf-8'))
            print(f"Received from server :: {reply}")
            return reply  # отправляем то что получилось после ответа
        except socket.error as e:
            print(e)

#   -------- Только Отправка Даты
    def send(self, data):
        try:
            print(f"Sending to server :: {data}")
            # json dumps преобразовать в байты для отправки
            self.client.send(json.dumps(data).encode('utf-8'))
            return  # Убираем попытку получения ответа
        except socket.error as e:
            print(e)
#   --------------------------------------

#n=Network()
#print(n.send({'message': 'pickle_base_server_client_network message from def send'}))
#print(n.send_and_rec({'message': 'pickle_base_server_client_network message from def send_and_rec'}))