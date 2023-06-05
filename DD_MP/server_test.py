import socket
import threading
#import time
#import _pickle as pickle
#import random
#import math
import pygame

# Constants
SERVER_IP = 'localhost'
PORT = 10000

W, H = 1600, 830
WIDHT_SERVER_WINDOW, HEIGHT_SERVER_ROOM = 300, 300  # Серверное окно

START_RADIUS = 7

pygame.init()  # запуск pygame
screen = pygame.display.set_mode((WIDHT_SERVER_WINDOW, HEIGHT_SERVER_ROOM))
clock = pygame.time.Clock()

# Dynamic variables
balls = []
connections = 0 # общее кол-во подключенных игроков
_id = 0 # id игрока
colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0),
          (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255),
          (0, 0, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255),
          (255, 0, 128), (128, 128, 128), (0, 0, 0)]

start_time = 0
game_time = "Starting Soon"
nxt = 1


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.players = {}

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen()

        threading.Thread(target=self.connect_handler).start()

        print(f"[SERVER] Server Prepare Config for Start with IP: {SERVER_IP}")

    # Обрабатываем входящие соединения (connect_handler)
    def connect_handler(self):
        while True:
            try:
                # -----ОБРАБОТЧИК СОБЫТИЙ-----
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        print('SERVER: STOPPED')
                # ----------------------------

                # Принимаем запрос нового клиента
                new_client, address = self.server.accept()
                new_client.setblocking(False)
                # Получаем идентификатор клиента
                data = new_client.recv(1024)
                name = data.decode("utf-8")
                _id = int(data.decode("utf-8"))
            except:
                pass

            if new_client not in self.players:
                self.players[new_client] = _id
                _id += 1
                print("[LOG]", _id, "connected to the server.")
                new_client.send(str(_id).encode('utf-8'))

            #color = colors[_id]
            #self.players[_id] = {"color":color, "score":0, "name":name}

            # pickle data and send initial info to clients
            #client.send(str.encode(str(current_id)))

# Попытка запустить сервер
try:
    S = Server(SERVER_IP, PORT)
    print("[SERVER] Started Successfully")
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()
