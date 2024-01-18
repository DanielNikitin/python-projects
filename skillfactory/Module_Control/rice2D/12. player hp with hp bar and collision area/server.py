import socket
import pickle
import time

from _thread import *

from server_config import *
from server_func import *
from player import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    server_socket.bind((server_ip, port))
except socket.error as e:
    print(f"Ошибка при привязке адреса: {e}")

server_socket.listen(24)
print("СЕРВЕР ЗАПУЩЕН")

spawn_tree()
spawn_ore()

def handle_client(connection, player_id):
    player = spawn_player(player_id)
    connection.send(pickle.dumps(player))

    extra_data = {"message": "Это первая информация!"}

    while True:
        try:
            received_data = pickle.loads(connection.recv(2048))
            print("Полученные данные:", received_data)

            if isinstance(received_data, dict):
                player_data = received_data["player"]
                message = received_data.get("p_action", "")

                if message == "change_text":
                    print("Меняем текст на экране")
                    extra_data = {"message": "Это вторая информация!"}

                elif message == "tree_delete":
                    print("Удаляем дерево")
                    delete_tree()

                elif message == "p_damage":
                    print("server :: -1 hp")

                elif message == "attack_player":
                    print("Атака другого игрока")


                if isinstance(player_data, Player):
                    player_list[player_id] = player_data
                    reply = list(player_list.values())

                    # Проверяем коллизию с другими игроками
                    check_collision(player_id)

                    # Вывод данных перед отправкой клиенту
                    print(f"Отправляются данные клиенту {player_id}: {reply}")

                    # Добавляем задержку перед отправкой данных клиенту
                    time.sleep(0.01)

                    connection.sendall(pickle.dumps((reply, tree_list, ore_list, extra_data)))

        except Exception as e:
            print(f"Ошибка обработки данных :: {e}")
            break

    print(f"Отключен :: {player_id}")
    # del player_list[player_id]  # удаляем игрока из мира
    player_list[player_id].status = "sleep"

    connection.close()

current_player_id = 0
while True:
    client_connection, client_address = server_socket.accept()
    print(f"Подключен: {client_address}")

    # Запускаем новый поток для каждого клиента
    start_new_thread(handle_client, (client_connection, current_player_id))

    # Увеличиваем счетчик для следующего игрока
    current_player_id += 1
