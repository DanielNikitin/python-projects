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


def threaded_client(client_conn):
    player = player_respawn()
    print(f"SERVER :: {player}")

    while True:
        try:
            # SEND DATA
            player_data = pickle.dumps(player)
            server_socket.send(player_data)
            print(f"SERVER SEND :: {player_data}")

            # LOAD DATA
        except:
            break

    print(f"Disconnected: {player.id} :: {player.name}")
    client_conn.close()


while True:  # ожидаем желаемых для подключения к серверу
    client_conn, addr = server_socket.accept()  # client_conn сокет для общения с подключенным клиентом
    print(f"Connected: {addr}")

    # Запускаем новый поток для каждого клиента
    start_new_thread(threaded_client, (client_conn,))
