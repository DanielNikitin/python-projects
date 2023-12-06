import pygame
import keyboard
import random


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

        self.status = "active"

        # Инициализируем инвентарь как словарь
        self.inventory = {"coins": 0}

        # Добавляем атрибут keys для хранения состояния клавиш
        self.keys = set()


    # ------ TERMINAL DATA
    def __str__(self):
        return f"Player({self.x}, {self.y}, {self.width}, {self.height}, {self.color}, {self.name}, {self._id})"

    def draw(self, screen):
        font = pygame.font.Font(pygame.font.get_default_font(), 20)  # Размер шрифта для никнейма

        if self.status == "sleep":
            # Если статус "sleep", рисуем горизонтальный прямоугольник 60, 35
            pygame.draw.rect(screen, self.color, (self.x, self.y, 60, 35))

            font_sleep = pygame.font.Font(pygame.font.get_default_font(), 15)  # Уменьшили размер шрифта для (sleep)
            text_sleep = font_sleep.render("(sleep)", True, (0, 0, 0))  # 0,0,0 - black color
            text_name = font.render(f"{self.name}", True, (0, 0, 0))  # 0,0,0 - black color

            text_sleep_rect = text_sleep.get_rect(center=(self.x + 25, self.y - 10))  # Центрируем надпись (sleep)
            text_name_rect = text_name.get_rect(center=(self.x + 25, self.y + 17.5))  # Центрируем надпись с именем

            screen.blit(text_sleep, text_sleep_rect.topleft)
            screen.blit(text_name, text_name_rect.topleft)

        elif self.status == 'active':
            # В противном случае рисуем текущий прямоугольник с размерами
            pygame.draw.rect(screen, self.color, self.rect)

            text = font.render(self.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + 25, self.y + 17.5))  # Центрируем надпись с именем

            screen.blit(text, text_rect.topleft)

        elif self.status == "h_pressed":
            pygame.draw.rect(screen, self.color, (self.x, self.y, 100, 100))  # Измененный размер 100x100

            font_h_pressed = pygame.font.Font(pygame.font.get_default_font(), 15)
            text_h_pressed = font_h_pressed.render("(h pressed)", True, (0, 0, 0))
            text_name = font.render(f"{self.name}", True, (0, 0, 0))

            text_h_pressed_rect = text_h_pressed.get_rect(center=(self.x + 50, self.y - 10))
            text_name_rect = text_name.get_rect(center=(self.x + 50, self.y + 70))

            screen.blit(text_h_pressed, text_h_pressed_rect.topleft)
            screen.blit(text_name, text_name_rect.topleft)


    def move(self):
        keys = pygame.key.get_pressed()

        # Очищаем множество клавиш при каждом движении
        #self.keys.clear()

        if keys[pygame.K_a]:
            self.x -= self.vel

        if keys[pygame.K_d]:
            self.x += self.vel

        if keys[pygame.K_w]:
            self.y -= self.vel

        if keys[pygame.K_s]:
            self.y += self.vel

        if keys[pygame.K_h]:
            print("player: n.send h_pressed")

        self.update()


    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
