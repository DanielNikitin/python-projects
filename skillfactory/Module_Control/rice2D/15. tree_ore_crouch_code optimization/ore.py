import pygame

class Ore:
    def __init__(self, x, y, width, height, color, _id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.id = _id
        self.hp = 2

    # ------ TERMINAL DATA
    def __str__(self):
        return f"Ore({self.x}, {self.y}, {self.width}, {self.height}, {self.color}, {self.id})"

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
