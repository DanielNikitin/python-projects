import socket
import select
import pygame as pg

HEADER_LENGHT = 10
HOST = ('localhost', 10000)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(HOST)
server.listen()
print('I am listening your connections!')

sockets_list = [server]
clients_list = {}

FPS = 100  # server speed

clock = pg.time.Clock()

def receive_msg(client: socket.socket):
    try:
        msg_header = client.recv(HEADER_LENGHT)
        if not len(msg_header):
            return False

        msg_lenght = int(msg_header.decode('UTF-8').strip())

        return {
            'header' : msg_header,
            'data' : client.recv(msg_lenght),
        }
    except:
        return False

while 1:
    clock.tick(FPS)
    rs, _, xs = select.select(sockets_list, [], sockets_list)
    for _socket in rs:
        if _socket == server:  # сервер получает данное сообщение
            client, addr = server.accept()  # получает сокет
            user = receive_msg(client)  # получает сообщение

            if user is False:
                continue
            sockets_list.append(client)
            clients_list[client] = user
            data = user['data']
            print(f'New connection from {addr} with data {data.decode("UTF-8")}')

        else:
            msg = receive_msg(client)
            print(msg)

            if msg is False:
                print(f'Connection from {addr} has been interrupted')
                sockets_list.remove(_socket)
                del clients_list[_socket]
                continue

            user = clients_list[_socket]

            for client in clients_list:
                    client.send(user["header"]+user["data"]+msg["header"]+msg["data"])

            for _socket in xs:
                sockets_list.remove(_socket)
                del clients_list[_socket]
