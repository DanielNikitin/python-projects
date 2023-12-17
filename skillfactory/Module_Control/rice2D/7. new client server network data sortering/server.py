# SERVER

import pickle

from _thread import *
from server_config import *
from server_func import *


try:
    server_socket.bind((server_ip, port))
except socket.error as e:
    print(str(e))
server_socket.listen(24)
print(f"SERVER STARTED :: {server_ip}, {port}")


def threaded_client(client_conn, player):
    player = player_respawn(player)  # respawn in the game world
    players_list[player] = player  # adding player into the :: players_list[ключ] = 'value'

    while True:
        try:
            # SEND PLAYER DATA
            player_data = pickle.dumps({'player': player, 'players_list': players_list})
            client_conn.send(player_data)
            print(f"SERVER SEND :: {player_data}")

            # LOAD DATA
            load_data = pickle.loads(client_conn.recv(2048))
            print(load_data)

            if not load_data:
                print("not player_data")
                break
            else:
                # UPDATE PLAYER CONDITION ON THE SERVER
                # --------------
                # --------------
                # --------------
                print("else")

        except socket.error as e:
            print(e)
        finally:
            print(f"Disconnected :: {player.name}, ID: {player.id}")
            client_conn.close()

current_player = 0
while True:  # ожидаем желаемых для подключения к серверу
    client_conn, addr = server_socket.accept()  # client_conn сокет для общения с подключенным клиентом
    print(f"Connected: {addr}")

    # Запускаем новый поток для каждого клиента
    start_new_thread(threaded_client, (client_conn, current_player))
    current_player += 1
