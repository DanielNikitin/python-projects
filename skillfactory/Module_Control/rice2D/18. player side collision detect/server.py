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

# -------- SOCKET SETUP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    server_socket.bind((server_ip, port))
except socket.error as e:
    print(f"Ошибка при привязке адреса: {e}")

server_socket.listen(24)
clock = pygame.time.Clock()
print("СЕРВЕР ЗАПУЩЕН")
print("---------------")
print("")


# -------- PLAYER
player_list = {}
names_list = ["DDFan", "Bob", "typesen", "kotik", "pups", "Bob2"]

def spawn_player(_id):
    x, y = random.randint(20, 350), random.randint(50, 350)
    width = random.randint(40, 50)
    height = random.randint(50, 70)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    name = random.choice(names_list)
    hp = 10

    return Player(x, y, width, height, color, name, _id, hp)

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

# -------- CIRCLE/RECTANGLE COLLISION DETECT
def is_rect_collision(obj1, obj2, hard_collision=True):
    if hard_collision:
        # Hard collision detection using rectangles
        return obj1.x < obj2.x + obj2.width and \
               obj1.x + obj1.width > obj2.x and \
               obj1.y < obj2.y + obj2.height and \
               obj1.y + obj1.height > obj2.y
    else:
        # Soft collision detection using circle-rectangle collision
        obj1_center = (obj1.x + obj1.width // 2, obj1.y + obj1.height // 2)
        obj2_center = (obj2.x + obj2.width // 2, obj2.y + obj2.height // 2)
        distance_squared = (obj1_center[0] - obj2_center[0])**2 + (obj1_center[1] - obj2_center[1])**2
        radius_sum_squared = (obj1.collision_radius + obj2.collision_radius)**2
        return distance_squared < radius_sum_squared

# -------- RECTANGLE CHECK TOUCHING (RECTANGLE COLLISION)
def get_touching_side(player, obj):
    player_left = player.x
    player_right = player.x + player.width
    player_top = player.y
    player_bottom = player.y + player.height

    obj_left = obj.x
    obj_right = obj.x + obj.width
    obj_top = obj.y
    obj_bottom = obj.y + obj.height

    # Check if rectangles are touching
    if (
        player_left < obj_right and
        player_right > obj_left and
        player_top < obj_bottom and
        player_bottom > obj_top
    ):
        # Calculate overlapping area
        overlap_left = max(player_left, obj_left)
        overlap_right = min(player_right, obj_right)
        overlap_top = max(player_top, obj_top)
        overlap_bottom = min(player_bottom, obj_bottom)

        # Calculate side lengths of the overlapping area
        overlap_width = overlap_right - overlap_left
        overlap_height = overlap_bottom - overlap_top

        # Determine which side has more overlap
        if overlap_width > overlap_height:
            if player.y > obj.y:
                return "top"
            else:
                return "bottom"
        else:
            if player.x > obj.x:
                return "left"
            else:
                return "right"
    else:
        return None

def is_touching(obj1, obj2):
    touching_side = get_touching_side(obj1, obj2)
    if touching_side:
        print(f"Touching: Игрок {obj1.name} касается объекта {obj2.id} стороной {touching_side}")

# -------- SPAWN TREE AND ORE
tree_list = spawn_tree()
ore_list = spawn_ore()

# -------- HANDLE CLIENT
def handle_client(connection, _id):
    current_id = _id
    player_data = spawn_player(current_id)
    connection.send(pickle.dumps(player_data))

    extra_data = {"message": "RICE2D | CLOSE TEST"}

    print(player_data)

    while True:
        try:
            clock.tick(1024)  # SERVER FPS LIMIT

            # -------- RECEIVED DATA
            received_data = pickle.loads(connection.recv(2048))
            #print("Полученные данные ::", received_data)

            if received_data.get("client_action") == "move":  # MOVE DIRECTION
                direction = received_data.get("direction")
                player_list[current_id].move(direction)

            if received_data.get("client_action") == "mode":
                position = received_data.get("position")
                player_list[current_id].change_position(position)  # CHANGE POSITION

            if received_data.get("client_hud") == "change_text":
                extra_data = {"message": "Rice2D | Close Test"}

            # -------- RECTANGLE COLLISION DETECT
            for player_id, player_obj in player_list.items():
                if player_id != current_id and is_rect_collision(player_data, player_obj, hard_collision=True):
                    print(f"Hard Collision: Игрок {current_id} столкнулся с игроком {player_id}")
                    continue
                elif player_id != current_id and is_rect_collision(player_data, player_obj, hard_collision=False):
                    print(f"Soft Collision: Игрок {current_id} рядом с игроком {player_id}")
                    continue

            for tree in tree_list:
                if is_rect_collision(player_data, tree, hard_collision=True):
                    print(f"Hard Collision: Игрок {current_id} столкнулся с деревом {tree.id}")
                    continue
                elif is_rect_collision(player_data, tree, hard_collision=False):
                    print(f"Soft Collision: Игрок {current_id} рядом с деревом {tree.id}")
                    continue

            for ore in ore_list:
                if is_rect_collision(player_data, ore, hard_collision=True):
                    print(f"Hard Collision: Игрок {current_id} столкнулся с рудой {ore.id}")
                    continue
                elif is_rect_collision(player_data, ore, hard_collision=False):
                    #print(f"Soft Collision: Игрок {current_id} рядом с рудой {ore.id}")
                    continue

            # -------- TOUCHING CHECK
            for player_id, player_obj in player_list.items():
                if player_id != current_id:
                    is_touching(player_data, player_obj)

            for tree in tree_list:
                is_touching(player_data, tree)

            for ore in ore_list:
                is_touching(player_data, ore)




            player_list[current_id] = player_data
            reply = list(player_list.values())

            # -------- DATA TO SEND
            data_to_send = reply, tree_list, ore_list, extra_data
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
        player_list[current_id].status = "sleep"
    connection.close()

# -------- WAITING CONNECTIONS
_id = 0
while True:
    client_connection, client_address = server_socket.accept()
    print(f"Подключен: {client_address}")

    start_new_thread(handle_client, (client_connection, _id))
    _id += 1