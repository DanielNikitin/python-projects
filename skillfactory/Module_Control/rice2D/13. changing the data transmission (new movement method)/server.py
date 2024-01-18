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
print("СЕРВЕР ЗАПУЩЕН")
print("---------------")
print("")

# -------------- PLAYER

#  Кортеж для хранения игроков
player_list = {}

# Список имён
names_list = ["DDFan", "Bob", "typesen", "kotik", "pups", "Bob2"]

def spawn_player(_id):
    x, y = 50, 50
    width = 50
    height = 60
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    name = random.choice(names_list)
    hp = 10

    return Player(x, y, width, height, color, name, _id, hp)

# -------------- HANDLE CLIENT

def handle_client(connection, _id):
    current_id = _id
    player_data = spawn_player(current_id)
    connection.send(pickle.dumps(player_data))
    extra_data = {"message": "Это первая информация!"}
    print(player_data)

    while True:
        try:
            received_data = pickle.loads(connection.recv(2048))
            print("Полученные данные ::", received_data)

            if received_data == "change_text":
                print("text is changed")
                extra_data = {"message": "Новый текст"}

            elif received_data.get("action") == "move":
                direction = received_data.get("direction")
                print("Moving to the Right")
                player_data.move(direction)

            player_list[current_id] = player_data
            reply = list(player_list.values())

            # Вывод данных перед отправкой клиенту
            data_to_send = reply, extra_data
            print(f"Отправляются данные клиенту {current_id}: {data_to_send}")

            # Добавляем задержку перед отправкой данных клиенту
            time.sleep(0.01)

            # Исправлено: используйте player_data вместо player
            connection.sendall(pickle.dumps(data_to_send))

        except Exception as e:
            print(f"Ошибка обработки данных :: {e}")
            break

    print(f"Отключен :: {current_id}")
    print("")
    # Исправлено: используйте current_id для проверки вместо player_list
    if current_id in player_list:
        player_list[current_id].status = "sleep"
    connection.close()

# Ожидаем подключения новых клиентов
_id = 0
while True:
    client_connection, client_address = server_socket.accept()
    print(f"Подключен: {client_address}")

    # Запускаем новый поток для каждого клиента
    start_new_thread(handle_client, (client_connection, _id))
    # Увеличиваем счетчик для следующего игрока
    _id += 1