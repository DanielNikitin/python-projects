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

# создаем одно дерево
spawn_tree()
print(tree_list)


def threaded_client(conn):

    while True:
        try:
            data_to_send = {'trees': 'ja derevo'}
            serialized_data = pickle.dumps(data_to_send)

            received_data = conn.recv(2048)  # получили байты
            loaded_data = pickle.loads(received_data)  # изменили байты в нормальный вид

            if not received_data:
                print("Disconnected")
                break
            else:
                print("Received: ", loaded_data)
                print("Sending : ", serialized_data)  # Отправляем данные как словарь

            conn.send(serialized_data)  # Отправляем данные

        except Exception as e:
            print(f"Error in threaded_client: {e}")
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected:", addr)

    start_new_thread(threaded_client, (conn,))