import pygame
import keyboard

class Player:
    def __init__(self, x, y, width, height, color, name, _id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

        self.name = name
        self.id = _id

        # Инициализируем инвентарь как словарь
        self.inventory = {"coins": 0}

        # Добавляем атрибут keys для хранения состояния клавиш
        self.keys = set()


    def __str__(self):
        return f"Player({self.x}, {self.y}, {self.width}, {self.height}, {self.color}, {self.name})"

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)  # player model

        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        text = font.render(self.name, True, (0, 0, 0))
        screen.blit(text, (self.x - -10, self.y - -20))  # nickname coordinate

    def move(self):
        keys = pygame.key.get_pressed()

        # Очищаем множество клавиш при каждом движении
        self.keys.clear()

        if keys[pygame.K_a]:
            self.x -= self.vel

        if keys[pygame.K_d]:
            self.x += self.vel

        if keys[pygame.K_w]:
            self.y -= self.vel

        if keys[pygame.K_s]:
            self.y += self.vel

        if keyboard.is_pressed('h'):
            print("data is sended to server")

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
