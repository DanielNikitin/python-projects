import pygame
#import random
import time


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

        self.last_status_change_time = 0
        self.delay_between_changes = 1000  # Задержка в миллисекундах (в данном случае 1 секунда)


    # ------ TERMINAL DATA
    def __str__(self):
        return f"Player({self.x}, {self.y}, {self.width}, {self.height}, {self.color}, {self.name}, {self.id})"


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

        elif self.status == 'crowl':
            pygame.draw.rect(screen, self.color, (self.x, self.y, 60, 35))

            text = font.render(self.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + 25, self.y + 17.5))  # Центрируем надпись с именем

            screen.blit(text, text_rect.topleft)

    def change_size(self):
        keys = pygame.key.get_pressed()  # текущее состояние всех клавиш

        if keys[pygame.K_h]:
            current_time = pygame.time.get_ticks()  # Получает текущее время в миллисекундах.
            time_since_last_change = current_time - self.last_status_change_time  # Вычисляет разницу между текущим временем и временем последнего изменения статуса.

            if time_since_last_change >= self.delay_between_changes:  # прошло достаточно времени?
                self.status = "crowl" if self.status == "active" else "active"  # меняем статус
                self.last_status_change_time = current_time  # Обновляет время последнего изменения статуса



    def move(self):
        keys = pygame.key.get_pressed()  # текущее состояние всех клавиш

        if keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_d]:
            self.x += self.vel
        if keys[pygame.K_w]:
            self.y -= self.vel
        if keys[pygame.K_s]:
            self.y += self.vel

        if keys[pygame.K_j]:
            self.y -= 50

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
