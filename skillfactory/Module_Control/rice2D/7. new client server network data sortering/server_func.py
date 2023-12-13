import random

from player import *

#  Кортеж для хранения игроков
players_list = {}

# Список имён
names_list = ["DDFan", "Bob", "typesen", "kotik", "pups", "Bob2"]

def player_respawn():  # создаем персонажа и спавним его в мире
    global players_list
    new_id = len(players_list) + 1  # increase id
    x, y = 50, 50
    width = 50
    height = 60
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    name = random.choice(names_list)

    player = Player(x, y, width, height, color, name, new_id)
    players_list[new_id] = player  # add to list
    return player