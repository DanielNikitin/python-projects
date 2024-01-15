import socket
import pickle

from _thread import *
from server_func import *

# pickle dumps преобразовать в байты для отправки
# pickle loads преобразовать байты в нормальный текст

server_ip = "localhost"
port = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))


# создадим 5 деревьев
spawn_tree()
spawn_ore()

s.listen(5)
print("SERVER STARTED")

def threaded_client(conn):
    # отправляем данные клиенту об этом
    conn.send(pickle.dumps((tree_list, ore_list)))

    while True:
        try:
            rec_data = conn.recv(2048)  # получили байты
            loaded_data = pickle.loads(rec_data)  # переводим в нормальный текст

            if not rec_data:
                print("Disconnected")
                break
            else:

                if loaded_data == 'r':
                    delete_tree()
                    delete_ore()

                print("Received: ", rec_data)
                print("Sending : ", (tree_list, ore_list))


            conn.sendall(pickle.dumps((tree_list, ore_list)))

        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected:", addr)

    start_new_thread(threaded_client, (conn,))