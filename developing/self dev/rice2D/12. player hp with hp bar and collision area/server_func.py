import random

from player import *
from tree import *
from ore import *

#  Кортеж для хранения игроков
player_list = {}

# Список имён
names_list = ["DDFan", "Bob", "typesen", "kotik", "pups", "Bob2"]

def spawn_player(_id):
    x, y = 50, 50
    width = 50
    height = 60
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    name = random.choice(names_list)
    hp = 10

    return Player(x, y, width, height, color, name, _id, hp)

def check_collision(player_id):
    current_player = player_list[player_id]
    for other_id, other_player in player_list.items():
        if player_id != other_id:
            distance = ((current_player.x - other_player.x) ** 2 + (current_player.y - other_player.y) ** 2) ** 0.5
            if distance < current_player.collision_radius + other_player.collision_radius:
                print(f"{player_id} внутри коллизии игрока {other_id}")

#   -------------- TREE
tree_list = []

def spawn_tree():
    for _id in range(1, 6):  # Создаем 5 деревьев
        x, y = random.randint(20, 350), random.randint(50, 350)
        width, height = random.randint(10, 20), random.randint(25, 55)
        color = (0, random.randint(0, 255), 0)

        new_tree = Tree(x, y, width, height, color, _id)
        tree_list.append(new_tree)

def delete_tree():
    if tree_list:
        tree_list.pop(0)
        print("Tree {_id} removed")


#   -------------- Stone ORE
ore_list = []

def spawn_ore():
    for _id in range(1, 6):  # Создаем 5
        x, y = random.randint(20, 350), random.randint(50, 350)
        width, height = 20, 20
        color = (128, 128, 128)

        new_ore = Ore(x, y, width, height, color, _id)
        ore_list.append(new_ore)

def delete_ore():
    if ore_list:
        ore_list.pop(0)
        print("Ore {_id} removed")