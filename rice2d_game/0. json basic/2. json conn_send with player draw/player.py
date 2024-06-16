import pygame

class Player:
    def __init__(self, player_id, x, y, width, height, color=(255, 0, 0)):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)

    def to_dict(self):
        return {
            "id": self.player_id,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "color": self.color
        }

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)