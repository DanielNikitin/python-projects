import socket
import pickle
import time
from _thread import *
from player import Player
from server_config import *
from server_func import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    server_socket.bind((server_ip, port))
except socket.error as e:
    print(f"Ошибка при привязке адреса: {e}")

server_socket.listen(24)
print("СЕРВЕР ЗАПУЩЕН")

def handle_client(connection, player_id):
    player = player_respawn(player_id)
    connection.send(pickle.dumps(player))

    while True:
        try:
            received_data = pickle.loads(connection.recv(2048))
            print("Полученные данные:", received_data)

            if isinstance(received_data, dict) and "player" in received_data:
                player_data = received_data["player"]
                message = received_data.get("message", "")

                if isinstance(player_data, Player):
                    players_list[player_id] = player_data
                    reply = list(players_list.values())

                    # Добавляем дополнительные данные на сервере
                    extra_data = {"message": "Это дополнительные данные с сервера!"}

                    # Вывод данных перед отправкой клиенту
                    print(f"Отправляются данные клиенту {player_id}: {reply}")

                    # Добавляем задержку перед отправкой данных клиенту
                    time.sleep(1)

                    connection.sendall(pickle.dumps((reply, extra_data)))

        except Exception as e:
            print(f"Ошибка обработки данных: {e}")
            break

    print(f"Отключен: {player_id}")
    # del players_list[player_id]  # удаляем игрока из мира

    connection.close()

current_player_id = 0
while True:
    client_connection, client_address = server_socket.accept()
    print(f"Подключен: {client_address}")

    # Запускаем новый поток для каждого клиента
    start_new_thread(handle_client, (client_connection, current_player_id))

    # Увеличиваем счетчик для следующего игрока
    current_player_id += 1
