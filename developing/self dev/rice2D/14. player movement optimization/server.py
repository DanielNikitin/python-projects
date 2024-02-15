import pygame
import socket
import pickle
import time
import random

from _thread import *

from server_config import *

from player import Player

# -------- SOCKET SETUP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    server_socket.bind((server_ip, port))
except socket.error as e:
    print(f"Ошибка при привязке адреса: {e}")

server_socket.listen(24)
clock = pygame.time.Clock()
print("СЕРВЕР ЗАПУЩЕН")
print("---------------")
print("")

# -------- PLAYER
player_list = {}
names_list = ["DDFan", "Bob", "typesen", "kotik", "pups", "Bob2"]

def spawn_player(_id):
    x, y = 50, 50
    width = 50
    height = 60
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    name = random.choice(names_list)
    hp = 10

    return Player(x, y, width, height, color, name, _id, hp)

# -------- HANDLE CLIENT
def handle_client(connection, _id):
    current_id = _id
    player_data = spawn_player(current_id)
    connection.send(pickle.dumps(player_data))
    extra_data = {"message": "Это первая информация!"}
    print(player_data)

    while True:
        try:
            clock.tick(1024)  # SERVER FPS LIMIT

            received_data = pickle.loads(connection.recv(2048))
            print("Полученные данные ::", received_data)

            if received_data.get("action") == "move":
                direction = received_data.get("direction")
                player_list[current_id].move(direction)

            if received_data.get("client_hud") == "change_text":
                print("text is changed")
                extra_data = {"message": "Новый текст"}

            player_list[current_id] = player_data
            reply = list(player_list.values())

            # Переменная для хранения данных
            data_to_send = reply, extra_data
            print(f"Отправляются данные клиенту {current_id}: {data_to_send}")

            # Отправка упакованных данных клиенту
            connection.sendall(pickle.dumps(data_to_send))

        except Exception as e:
            print(f"Ошибка обработки данных :: {e}")
            break

# -------- DISCONNECT CLIENT
    print(f"Отключен :: {current_id}")
    print("")

    if current_id in player_list:
        player_list[current_id].status = "sleep"
    connection.close()

# -------- WAITING CONNECTIONS
_id = 0
while True:
    client_connection, client_address = server_socket.accept()
    print(f"Подключен: {client_address}")

    start_new_thread(handle_client, (client_connection, _id))
    _id += 1