import socket
import threading
#import time
#import _pickle as pickle
#import random
#import math

# Constants
SERVER_IP = 'localhost'
PORT = 10000

W, H = 1600, 830

START_RADIUS = 7

# Dynamic variables
balls = []
connections = 0
_id = 0
colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0),
          (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255),
          (0, 0, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255),
          (255, 0, 128), (128, 128, 128), (0, 0, 0)]
start = False
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
        print(f"[SERVER] Server Started with IP: {SERVER_IP}")

    # Обрабатываем входящие соединения (connect_handler)
    def connect_handler(self, conn, _id):
        global connections, balls, game_time, nxt, start

        current_id = _id

        while True:
            client, address = self.server.accept()

            # Получаем идентификатор клиента
            data = client.recv(16)
            name = data.decode("utf-8")
            current_id = int(data.decode("utf-8"))

            if client not in self.players:
                self.players[client] = _id
                connections += 1
                _id += 1
                print("[LOG]", current_id, "connected to the server.")
                client.send(str(current_id).encode('utf-8'))

            color = colors[current_id]
            self.players[current_id] = {"name":name}

            # pickle data and send initial info to clients
            conn.send(str.encode(str(current_id)))  # остановился тут


# Попытка запустить сервер
try:
    S = Server(SERVER_IP, PORT)
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()