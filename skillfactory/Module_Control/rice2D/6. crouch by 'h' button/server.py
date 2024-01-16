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
            loaded_data = pickle.loads(conn.recv(2048))
            players_list[player] = loaded_data

            if not loaded_data:
                print(f"NOT DATA, DISCONNECTED: {player}")
                break

            else:

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
while True:
    conn, addr = s.accept()
    print(f"Connected: {addr}")

    # Запускаем новый поток для каждого клиента
    start_new_thread(threaded_client, (conn, currentPlayer))

    # Увеличиваем счетчик для следующего игрока
    currentPlayer += 1
