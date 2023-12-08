import socket
import json

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


def threaded_client(conn, three):
    # json dumps преобразовать в байты для отправки
    conn.send(json.dumps(spawn_three(three)).encode('utf-8'))  # отправляем спавн дерева и кодируем в байты

    while True:
        try:
            rec_data = conn.recv(2048).decode('utf-8')  # получили байты
            loaded_data = json.loads(rec_data)  # изменили байты в нормальный вид

            reply = rec_data  # отправили новую data

            if not rec_data:
                print("Disconnected")
                break
            else:
                print("Received: ", rec_data)
                print("Sending : ", reply)

            conn.sendall(json.dumps(reply).encode('utf-8'))

        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected:", addr)

    start_new_thread(threaded_client, (conn, Three))