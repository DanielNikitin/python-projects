import socket
import pickle
import random

from _thread import *
from player import Player
from server_config import *
from server_func import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))

s.listen(24)
print("SERVER STARTED")

def threaded_client(conn, player):
    conn.send(pickle.dumps(player_respawn(player)))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if data == "h_pressed":
                print(f"Key 'h' pressed for player: {player}")
                players_list[player].status = "h_pressed"

            players_list[player] = data

            if not data:
                print(f"NOT DATA, DISCONNECTED: {player}")
                break
            else:
                reply = list(players_list.values())

            conn.sendall(pickle.dumps(reply))

        except:
            break

    print(f"Disconnected: {player}")
    players_list[player].status = "sleep"
    conn.close()

currentPlayer = 0
while True:  # ожидаем желаемых для подключения к серверу
    conn, addr = s.accept()  # принимаем их запрос на подключение
    print(f"Connected: {addr}")

    # Запускаем новый поток для каждого клиента
    start_new_thread(threaded_client, (conn, currentPlayer))

    # Увеличиваем счетчик для следующего игрока
    currentPlayer += 1
