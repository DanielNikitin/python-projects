import pygame
import socket
import json

import _thread
import time
import random

from server_config import *

clock = pygame.time.Clock()

def handle_client(client_socket, _id):
    current_id = _id

    player_data = {"player": "Дата об игроке"}
    player_data_send = json.dumps(player_data).encode('utf-8')
    client_socket.send(player_data_send)

    try:
        while True:
            clock.tick(120)  # Server FPS

            # -------- RECEIVED DATA
            received_data = client_socket.recv(1024)  # encoded data from client
            print(f"Received from client [{current_id}]: {received_data}")

            if not received_data:
                print(f"Client [{current_id}] disconnected")
                break

            decoded_data = json.loads(received_data.decode('utf-8'))
            print(decoded_data)

            # Check for disconnect command
            if decoded_data.get("action") == "disconnect":
                print(f"Client [{current_id}] requested disconnect")
                break

            # Check for disconnect command
            if decoded_data.get("action") == "move_right":
                print(f"Client [{current_id}] want to move right")

            # -------- DATA TO SEND
            reply = {"players": "Дата для об игроках"}
            data_to_send = json.dumps(reply).encode('utf-8')
            client_socket.send(data_to_send)

            # -------- Handle Client FPS Counter
            if FPS_Counter:
                fps = clock.get_fps()
                if fps > 0:
                    print(f"Server FPS[{current_id}]: {fps:.2f}")

    except socket.error as e:
        print(f"Ошибка при обработке клиента [{current_id}]: {e}")
    finally:
        print(f"Закрытие соединения с клиентом [{current_id}]")
        client_socket.close()



def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        server.bind((server_ip, port))
        server.listen(25)
        print(f"{server}")
        print("Server listening for connections...")

        _id = 0
        # -------- WAITING CONNECTIONS
        while True:
            client_socket, client_addr = server.accept()
            print(f"Accepted connection from {client_addr}, ID:[{_id}]")

            _thread.start_new_thread(handle_client, (client_socket, _id))
            _id += 1

    except socket.error as e:
        print(f"Ошибка при привязке адреса: {e}")


start_server()
