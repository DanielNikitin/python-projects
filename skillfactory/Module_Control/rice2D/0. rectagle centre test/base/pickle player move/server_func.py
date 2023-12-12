import random

from tree import Tree
from ore import Ore
from player import Player

tree_list = []
ore_list = []

#  Кортеж для хранения игроков
player_list = {}

# Список имён
names_list = ["DDFan", "Bob", "typesen", "kotik", "pups", "Bob2"]

#   -------------- PLAYER

def player_respawn(_id):  # создаем персонажа и спавним его в мире
    x, y = 50, 50
    width = 50
    height = 60
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
   #name = random.choice(names_list)

    return Player(x, y, width, height, color, _id)  # получаем все данные после респавна

#   -------------- TREE
def spawn_tree():
    for _id in range(1, 3):  # Создаем 5 деревьев
        x, y = random.randint(20, 350), random.randint(50, 350)
        width, height = random.randint(10, 20), random.randint(25, 55)
        color = (0, random.randint(0, 255), 0)

        new_tree = Tree(x, y, width, height, color, _id)
        tree_list.append(new_tree)

def delete_tree():
    if tree_list:
        tree_list.pop(0)
        print("Tree {_id} removed")


#   -------------- ORE
def spawn_ore():
    for _id in range(1, 3):  # Создаем 10
        x, y = random.randint(20, 350), random.randint(50, 350)
        width, height = 20, 20
        color = (128, 128, 128)

        new_ore = Ore(x, y, width, height, color, _id)
        ore_list.append(new_ore)

def delete_ore():
    if ore_list:
        ore_list.pop(0)
        print("Ore {_id} removed")

