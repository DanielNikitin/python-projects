import socket
import pickle
import random

from _thread import *
from player import Player
from server_config import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))

s.listen(24)
print("SERVER STARTED")

#  Кортеж для хранения игроков
players_list = {}

# Список имён
names_list = ["DDFan", "Bob", "typesen", "kotik", "pups", "Bob2"]

def player_respawn(_id):  # создаем персонажа и спавним его в мире
    x, y = 50, 50
    width = 50
    height = 50
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    name = random.choice(names_list)

    return Player(x, y, width, height, color, name, _id)  # получаем все данные после респавна

def threaded_client(conn, player):  # Ожидание подключения клиентов
    conn.send(pickle.dumps(player_respawn(player)))  # Клиенту отправляется начальное состояние игрока через pickle

    while True:  # Сервер ожидает и принимает данные от клиента,
        # обновляет состояние игрока и отправляет обновленные данные всем клиентам
        try:
            data = pickle.loads(conn.recv(2048))  # получаем данные от клиента которые уже сериализованны pickle
            players_list[player] = data  # записываем состояние игрока в players

            if not data:
                print(f"NOT DATA, DISCONNECTED: {player}")
                break

            else:

                # Отправляем обновленные данные всем клиентам
                reply = list(players_list.values())
                #print(f"Sending data to {player} :: {reply}")

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print(f"Disconnected: {player}")
    #del players_list[player]  # удаляем игрока из мира
    players_list[player].status = "sleep"  # Устанавливаем статус "sleep"

    conn.close()

currentPlayer = 0
while True:  # ожидаем желаемых для подключения к серверу
    conn, addr = s.accept()  # принимаем их запрос на подключение
    print(f"Connected: {addr}")

    # Запускаем новый поток для каждого клиента
    start_new_thread(threaded_client, (conn, currentPlayer))

    # Увеличиваем счетчик для следующего игрока
    currentPlayer += 1
