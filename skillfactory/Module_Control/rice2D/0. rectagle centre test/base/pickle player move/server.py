import socket
import pickle

from _thread import *
from server_func import *
<<<<<<<< HEAD:skillfactory/Module_Control/rice2D/0. rectagle centre test/base/pickle player tree ore/server.py

# pickle dumps преобразовать в байты для отправки
# pickle loads преобразовать байты в нормальный текст
========
from player import Player
>>>>>>>> 63354c805457dc2a57d518145a048f73cbb7af15:skillfactory/Module_Control/rice2D/0. rectagle centre test/base/pickle player move/server.py

server_ip = "localhost"
port = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    s.bind((server_ip, port))
except socket.error as e:
    print(str(e))


<<<<<<<< HEAD:skillfactory/Module_Control/rice2D/0. rectagle centre test/base/pickle player tree ore/server.py
# создадим 5 деревьев
spawn_tree()
spawn_ore()

========
>>>>>>>> 63354c805457dc2a57d518145a048f73cbb7af15:skillfactory/Module_Control/rice2D/0. rectagle centre test/base/pickle player move/server.py
s.listen(5)
print("SERVER STARTED")


def threaded_client(conn):
<<<<<<<< HEAD:skillfactory/Module_Control/rice2D/0. rectagle centre test/base/pickle player tree ore/server.py
    player_id = len(player_list) +1
    # отправляем данные клиенту об этом
    conn.send(pickle.dumps((tree_list, ore_list)))
========
    # отправляем данные клиенту об этом
>>>>>>>> 63354c805457dc2a57d518145a048f73cbb7af15:skillfactory/Module_Control/rice2D/0. rectagle centre test/base/pickle player move/server.py

    while True:
        try:
            rec_data = conn.recv(2048)  # получили байты
            loaded_data = pickle.loads(rec_data)  # переводим в нормальный текст

            if not rec_data:
                print("Disconnected")
                break
            else:
<<<<<<<< HEAD:skillfactory/Module_Control/rice2D/0. rectagle centre test/base/pickle player tree ore/server.py
                handle_client_action(loaded_data, player_id)
========
>>>>>>>> 63354c805457dc2a57d518145a048f73cbb7af15:skillfactory/Module_Control/rice2D/0. rectagle centre test/base/pickle player move/server.py

                print("Received: ", rec_data)
                print("Sending : ", (tree_list, ore_list))


<<<<<<<< HEAD:skillfactory/Module_Control/rice2D/0. rectagle centre test/base/pickle player tree ore/server.py
            conn.sendall(pickle.dumps((tree_list, ore_list)))
========
            conn.sendall(pickle.dumps((tree_list)))
>>>>>>>> 63354c805457dc2a57d518145a048f73cbb7af15:skillfactory/Module_Control/rice2D/0. rectagle centre test/base/pickle player move/server.py

        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected:", addr)

    start_new_thread(threaded_client, (conn,))