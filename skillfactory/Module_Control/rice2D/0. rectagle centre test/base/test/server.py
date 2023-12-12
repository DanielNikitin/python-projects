import socket
import pickle

from _thread import *
from server_func import *


server_ip = "localhost"
port = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))

s.listen(24)
print("SERVER STARTED")


def threaded_client(conn):
    # pickle dumps преобразовать в байты для отправки
    # создаем одно дерево
    tree_list = spawn_tree()

    # отправляем данные клиенту об этом
    conn.send(pickle.dumps({"trees": tree_list}))

    while True:
        try:
            rec_data = conn.recv(2048)  # получили байты
            loaded_data = pickle.loads(rec_data)  # изменили байты в нормальный вид
            tree_list, ore_list, player_data = loaded_data

            if not rec_data:
                print("Disconnected")
                break
            else:
                print("Received: ", rec_data)
                print("Sending : ", {"trees": tree_list})  # Отправляем данные как словарь

            conn.sendall(pickle.dumps({"trees": tree_list}))  # Отправляем данные как словарь

        except Exception as e:
            print(f"Error in threaded_client: {e}")
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected:", addr)

    start_new_thread(threaded_client, (conn,))