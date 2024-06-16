import pygame

class Player():
    def __init__(self, x, y, width, height, color, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

        self.name = name

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)  # player model

        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = font.render(self.name, True, (0, 0, 0))
        win.blit(text, (self.x, self.y - 20))  # nickname coordinate


    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.vel

        if keys[pygame.K_d]:
            self.x += self.vel

        if keys[pygame.K_w]:
            self.y -= self.vel

        if keys[pygame.K_s]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
