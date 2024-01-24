import pygame
import socket
import pickle

import time
import random
import math

from _thread import *

from server_config import *

from player import Player
from tree import Tree
from ore import Ore
from trap import Trap

from collisions import *
from hp_analyzer import *

# -------- SOCKET SETUP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    server_socket.bind((server_ip, port))
except socket.error as e:
    print(f"Ошибка при привязке адреса: {e}")

server_socket.listen(24)
print("СЕРВЕР ВКЛЮЧЕН")
print("---------------")

clock = pygame.time.Clock()

# -------- PLAYER
player_list = {}
names_list = ["DDFan", "Bob", "typesen", "kotik", "pups", "Bob2"]

def spawn_player(_id):
    x, y = random.randint(20, 350), random.randint(50, 350)
    width = 50
    height = 70
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    name = random.choice(names_list)
    hp = 6
    vel = 2

    return Player(x, y, width, height, color, name, _id, hp, vel)

# -------- TREE
def spawn_tree():
    tree_list = []
    for _id in range(1, 2):
        x, y = random.randint(20, 350), random.randint(50, 350)
        width, height = random.randint(10, 20), random.randint(25, 55)

        # Generate a random shade of green
        green_component = random.randint(50, 255)
        color = (0, green_component, 0)

        tree = Tree(x, y, width, height, color, _id)
        tree_list.append(tree)

    return tree_list

# -------- ORE
def spawn_ore():
    ore_list = []
    for _id in range(1, 2):
        x, y = random.randint(20, 350), random.randint(50, 350)
        width, height = 30, 30

        # Generate a random shade of grey
        grey_component = random.randint(90, 150)
        color = (grey_component, grey_component, grey_component)

        ore = Ore(x, y, width, height, color, _id)
        ore_list.append(ore)

    return ore_list

# -------- TRAP
def spawn_trap():
    trap_list = []
    for _id in range(1, 2):
        x, y = random.randint(20, 350), random.randint(50, 350)
        width, height = random.randint(25, 35), random.randint(25, 35)

        # Generate a random shade of red (R component should be in the range [50, 255])
        red_component = random.randint(50, 255)
        color = (red_component, 0, 0)

        trap = Trap(x, y, width, height, color, _id)
        trap_list.append(trap)

    return trap_list

# -------- SPAWN TREE AND ORE
tree_list = spawn_tree()
ore_list = spawn_ore()
trap_list = spawn_trap()

# -------- HANDLE CLIENT
def handle_client(connection, _id):
    current_id = _id
    player_data = spawn_player(current_id)  # data about player to player_data
    connection.send(pickle.dumps(player_data))  # sending to client player_data

    info_data = {'info_data': 'RICE2D | DEV MODE'}
    #other_data = {'other_data': 'hud data is ok'}

    # Trap settings
    in_trap = False
    damage_timer = pygame.time.get_ticks()
    damage_interval = 300  # Интервал урона в миллисекундах (1000 = 1 секунда)

    while True:
        try:
            clock.tick(120)  # SERVER FPS LIMIT
           # fps = clock.get_fps()
           # if fps > 0:
          #      print(f"Server FPS: {fps:.2f}")

            # -------- RECEIVED DATA
            received_data = pickle.loads(connection.recv(640))
            #print("Полученные данные ::", received_data)

            if received_data.get("client_action") == "move":  # MOVE DIRECTION
                direction = received_data.get("direction")
                player_list[current_id].move(direction)

            if received_data.get("client_action") == "mode":
                position = received_data.get("position")
                player_list[current_id].change_position(position)  # CHANGE POSITION

            if received_data.get("client_hud") == "change_text":
                info_data = {'info_data': 'Rice2D | DEV MODE'}


            # -------- RECTANGLE COLLISION DETECT
            # ---- player
            for other_id, other_player in player_list.items():
                if current_id != other_id and rectangle_collision(player_data, other_player):
                    #print(f"Rectangle Collision: Игрок {current_id} столкнулся с игроком {other_id}")
                    continue
                elif current_id != other_id and circle_collision(player_data, other_player):
                    #print(f"Circle Collision: Игрок {current_id} рядом с игроком {other_id}")
                    continue

            # ---- tree
            for tree in tree_list:
                if rectangle_collision(player_data, tree):
                    #print(f"Rectangle Collision: Игрок {current_id} столкнулся с деревом {tree.id}")
                    continue
                elif circle_collision(player_data, tree):
                    #print(f"Circle Collision: Игрок {current_id} рядом с деревом {tree.id}")
                    continue

            # ---- ore
            for ore in ore_list:
                if rectangle_collision(player_data, ore):
                    #print(f"Rectangle Collision: Игрок {current_id} столкнулся с рудой {ore.id}")
                    continue
                elif circle_collision(player_data, ore):
                    #print(f"Circle Collision: Игрок {current_id} рядом с рудой {ore.id}")
                    continue

            # ---- trap
            for trap in trap_list:
                if rectangle_collision(player_data, trap):
                    if not in_trap:
                        in_trap = True
                        print(in_trap)

            # Проверка таймера для урона
            if in_trap and pygame.time.get_ticks() - damage_timer >= damage_interval:
                player_data.hp -= 1
                damage_timer = pygame.time.get_ticks()  # Сбрасываем таймер урона

            # Проверка, если игрок вышел из ловушки
            if not any(rectangle_collision(player_data, trap) for trap in trap_list):
                in_trap = False
                print(in_trap)

            # -------- TOUCHING CHECK
            # ---- player
            for other_id, other_player in player_list.items():
                if current_id != other_id:
                    is_touching(player_data, other_player)

            # ---- tree
            for tree in tree_list:
                is_touching(player_data, tree)

            # ---- ore
            for ore in ore_list:
                is_touching(player_data, ore)

            # ---- trap
            for trap in trap_list:
                is_touching(player_data, trap)

            # -------- PLAYER ANALYSING
            hp_data = analyze_player_health(player_data)
            other_data = {'other_data': str(player_data.vel)}

            # -------- DATA TO SEND
            # Обновление информации о текущем игроке в словаре player_list
            player_list[current_id] = player_data
            reply = list(player_list.values())

            data_to_send = (reply,
                            tree_list,
                            ore_list,
                            trap_list,

                            info_data,
                            other_data,
                            hp_data)
            #print(f"Отправляются данные клиенту {current_id}: {data_to_send}")

            # Отправка упакованных данных клиенту
            connection.sendall(pickle.dumps(data_to_send))

        except Exception as e:
            print(f"Ошибка обработки данных :: {e}")
            break

# -------- DISCONNECT CLIENT
    print(f"Отключен :: {current_id}")
    print("")

    if current_id in player_list:
        if player_list[current_id].status != "died":
            player_list[current_id].status = "sleep"
    connection.close()

# -------- WAITING CONNECTIONS
_id = 0
while True:
    print("Ожидаем подключения")
    print("---------------")

    client_connection, client_address = server_socket.accept()
    print(f"Подключен: {client_address}")

    start_new_thread(handle_client, (client_connection, _id))
    _id += 1