import pygame
import random

from tree import Tree
from ore import Ore

tree_list = []
ore_list = []
#player_key = []

player_id = []
player_list = []

# ---------------- PLAYER

#def player_move():

 #   if player_key == 'up':
  #      self.x -= self.vel
   # if player_key == 'left':
  #      self.x += self.vel
  #  if player_key == 'down':
    #    self.y -= self.vel
   # if player_key == 'right':
   #     self.y += self.vel


#   -------------- TREE
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
def spawn_ore():
    for _id in range(1, 11):  # Создаем 10
        x, y = random.randint(20, 350), random.randint(50, 350)
        width, height = 20, 20
        color = (128, 128, 128)

        new_ore = Ore(x, y, width, height, color, _id)
        ore_list.append(new_ore)

def delete_ore():
    if ore_list:
        ore_list.pop(0)
        print("Ore {_id} removed")

def handle_client_action(action, player_id):
    if action == 'r':
        delete_tree()

