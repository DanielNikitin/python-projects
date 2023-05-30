import time
import socket
import threading

#Eboisky 2023

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.all_client = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen(0)
        # Поток connect_handler для отслеживания нового соединения
        threading.Thread(target=self.connect_handler).start()
        print('****SERVER STARTED****')

    # Обрабатываем входящие соединения (connect_handler)
    def connect_handler(self):
        while True:
            # если клиент подсоединяется то = сервер принимает запрос
            client, address = self.server.accept()
            # если клиент новый и не состоит в списке
            if client not in self.all_client:
                # добавляем в список
                self.all_client.append(client)
                # запускаем новый поток обработки сообщений message_handler
                # передаем клиентский сокет args=(client,)) и запускаем поток .start()
                threading.Thread(target=self.message_handler, args=(client,)).start()
                # отправляем клиенту используя его сокет (client, address) сообщение об подключении
                client.send('Connection successed!'.encode('utf-8'))
            time.sleep(1)

    # Обрабатываем отправленный текст
    def message_handler(self, client_socket):
        while True:
            # принимаем сообщение от клиента в кол-ве байт 1024
            message = client_socket.recv(1024)
            print(message)

            # Удаляем текущий сокет
            if message == b'exit':
                self.all_client.remove(client_socket)
                break  # закончить connect and message_handler

            # Если сообщение не содержит 'exit'
            for client in self.all_client:
                # не является-ли клиент сокетом, чтобы не отправить сообщение самому себе
                if client != client_socket:
                    client.send(message)
                time.sleep(1)


myserver = Server('127.0.0.1', 10000)
