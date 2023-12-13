import random

from tree import *

tree_list = []

def spawn_tree():
    x, y = 50, 50
    width, height = 30, 50
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    new_tree = Tree(x, y, width, height, color, len(tree_list) + 1)
    tree_list.append(new_tree)
    return new_tree