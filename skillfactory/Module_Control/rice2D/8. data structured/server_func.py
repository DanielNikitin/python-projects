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