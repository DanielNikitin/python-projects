import random

from three import *

three_list = []

def spawn_three(_id):
    x, y = 50, 50
    width = 30
    height = 50
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    return Three(x, y, width, height, color, _id)