import socket
import pickle
from _thread import *
from player import Player
from server_config import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))

s.listen(3)
print("SERVER STARTED")

#  Кортеж для хранения игроков
players_list = {}

def player_respawn(_id):
    x, y = 50, 50
    width = 50
    height = 50
    color = (0, 255, 0)
    name = 'meow'
    return Player(x, y, width, height, color, name, _id)

def threaded_client(conn, player):  # Ожидание подключения клиентов
    conn.send(pickle.dumps(player_respawn(player)))  # Клиенту отправляется начальное состояние игрока через pickle

    while True:  # Сервер ожидает и принимает данные от клиента,
        # обновляет состояние игрока и отправляет обновленные данные всем клиентам
        try:
            data = pickle.loads(conn.recv(2048))  # получаем данные от клиента которые уже сериализованны pickle
            print(data)
            players_list[player] = data  # записываем состояние игрока в players

            if not data:
                print(f"Disconnected: {player}")
                break

            else:

                # Отправляем обновленные данные всем клиентам
                #reply = list(players_list.values())
                updated_data = list(players_list.values())
                print(f"Sending data to {player} :: {reply}")

            conn.sendall(pickle.dumps(updated_data))

        except:
            break

    print(f"Disconnected: {player}")
    #del players_list[player]
    conn.close()

currentPlayer = 0
while True:  # ожидаем желаемых для подключения к серверу
    conn, addr = s.accept()  # принимаем их запрос на подключение
    print(f"Connected: {addr}")

    # Запускаем новый поток для каждого клиента
    start_new_thread(threaded_client, (conn, currentPlayer))

    # Увеличиваем счетчик для следующего игрока
    currentPlayer += 1
