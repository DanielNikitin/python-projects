import random

from player import *

#  Кортеж для хранения игроков
players_list = {}

# Список имён
names_list = ["DDFan", "Bob", "typesen", "kotik", "pups", "Bob2"]

def player_respawn(_id):
    x, y = 50, 50
    width = 50
    height = 60
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    name = random.choice(names_list)

    return Player(x, y, width, height, color, name, _id)

from tree import *

tree_list = []

#   -------------- TREE
def spawn_tree():
    for _id in range(1, 6):  # Создаем 5 деревьев
        x, y = random.randint(20, 350), random.randint(50, 350)
        width, height = random.randint(10, 20), random.randint(25, 55)
        color = (0, random.randint(0, 255), 0)

        new_tree = Tree(x, y, width, height, color, _id)
        tree_list.append(new_tree)