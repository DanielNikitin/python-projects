import socket
import pickle

from _thread import *
from server_func import *
from player import Player

server_ip = "localhost"
port = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))


s.listen(5)
print("SERVER STARTED")


def threaded_client(conn):
    # отправляем данные клиенту об этом

    while True:
        try:
            rec_data = conn.recv(2048)  # получили байты
            loaded_data = pickle.loads(rec_data)  # переводим в нормальный текст

            if not rec_data:
                print("Disconnected")
                break
            else:

                print("Received: ", rec_data)
                print("Sending : ", (tree_list, ore_list))


            conn.sendall(pickle.dumps((tree_list)))

        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected:", addr)

    start_new_thread(threaded_client, (conn,))