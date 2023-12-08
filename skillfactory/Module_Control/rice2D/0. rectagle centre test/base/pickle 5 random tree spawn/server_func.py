import random

from tree import Tree

tree_list = []

def spawn_trees():
    for _id in range(1, 6):  # Создаем 5 деревьев
        x, y = random.randint(20, 350), random.randint(50, 350)
        width, height = 30, 50
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        new_tree = Tree(x, y, width, height, color, _id)
        tree_list.append(new_tree)