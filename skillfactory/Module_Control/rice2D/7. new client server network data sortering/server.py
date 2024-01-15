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
<<<<<<< Updated upstream
    player = player_respawn(player)  # respawn in the game world
    players_list[player] = player  # adding player into the :: players_list[ключ] = 'value'
=======
    player = player_respawn(player)  # respawn player in the game world
    print(f"PLAYER SPAWNED :: {player}")

    # SEND PLAYER DATA
    player_data = pickle.dumps({'player': player, 'players_list': players_list})
    client_conn.send(player_data)
    print(f"SERVER SEND :: {player_data}")
>>>>>>> Stashed changes

    while True:
        try:
            # LOAD DATA
            from_client = pickle.loads(client_conn.recv(2048))
            #print(from_client)

            players_list[player] = player  # adding player into the :: players_list[ключ] = 'value'
            #print(f"PLAYERS LIST :: {players_list}")

            #player_data_received = from_client.get('player', {})
            #print(f"PLAYER DATA FROM CLIENT :: {player_data_received}")

            #players_data_received = from_client.get('players_list', {})
            #print(f"PLAYERS DATA FROM CLIENT :: {players_data_received}")

            if not from_client:
                print("not player_data")
                break
            else:
<<<<<<< Updated upstream
                # UPDATE PLAYER CONDITION ON THE SERVER
                # --------------
                # --------------
                # --------------
                print("else")
=======
                reply = list(players_list.values())
                print(players_list)
>>>>>>> Stashed changes

            client_conn.send(pickle.dumps(reply))

        except Exception:
            print(f"Disconnected :: {player.name}, ID: {player.id}")
            client_conn.close()

current_player = 0
while True:  # ожидаем желаемых для подключения к серверу
    client_conn, addr = server_socket.accept()  # client_conn сокет для общения с подключенным клиентом
    print(f"Connected: {addr}")

    # Запускаем новый поток для каждого клиента
    start_new_thread(threaded_client, (client_conn, current_player))
    current_player += 1
