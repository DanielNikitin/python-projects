import pygame
#import random
import time


class Player:
    def __init__(self, x, y, width, height, color, name, _id, hp, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.name = name
        self.id = _id
        self.vel = vel  # character speed

        self.hp = hp  # если hp=hp то берем данные из сервера

        self.collision_radius = 50
        self.collision_visib = True  # in dev


        self.status = "active"

        # -------- CROUCH CONSTANT
        self.last_status_change_time = 0
        self.delay_between_changes = 300  # Задержка в миллисекундах (в данном случае 0.3 секунды)

        self.blocked_directions = {"Up": False, "Left": False, "Down": False, "Right": False}

    # -------- TERMINAL DATA
    def __str__(self):
        return f"Player({self.x}, {self.y}, {self.width}, {self.height}, {self.color}, {self.name}, ID:{self.id}, HP:{self.hp}, VEL:{self.vel})"

    # -------- DRAW
    def draw(self, screen):

        self.draw_collision(screen)  # collision area

        font = pygame.font.Font(pygame.font.get_default_font(), 20)  # Размер шрифта для никнейма

        # ---- active
        if self.status == 'active':
            pygame.draw.rect(screen, self.color, self.rect)
            text = font.render(self.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + 25, self.y + 17.5))  # Центрируем надпись с именем
            screen.blit(text, text_rect.topleft)

        # ---- sleep
        elif self.status == "sleep":
            # Если статус "sleep", рисуем горизонтальный прямоугольник 60, 35
            pygame.draw.rect(screen, self.color, (self.x, self.y, 60, 35))

            font_sleep = pygame.font.Font(pygame.font.get_default_font(), 12)  # Уменьшили размер шрифта для (sleep)
            text_sleep = font_sleep.render("(sleep)", True, (0, 0, 0))  # 0,0,0 - black color
            text_name = font.render(f"{self.name}", True, (0, 0, 0))  # 0,0,0 - black color

            text_sleep_rect = text_sleep.get_rect(center=(self.x + 30, self.y + 45))  # Центруем надпись (sleep)
            text_name_rect = text_name.get_rect(center=(self.x + 25, self.y + 17.5))  # Центруем надпись с именем

            screen.blit(text_sleep, text_sleep_rect.topleft)
            screen.blit(text_name, text_name_rect.topleft)

        # ---- crouch
        elif self.status == 'crouch':
            pygame.draw.rect(screen, self.color, (self.x, self.y, 60, 35))

            text = font.render(self.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + 25, self.y + 17.5))  # Центрируем надпись с именем

            screen.blit(text, text_rect.topleft)

        # ---- died
        elif self.status == 'died':
            pygame.draw.rect(screen, self.color, (self.x, self.y, 80, 40))  # Примерный размер для "died"

            font_died = pygame.font.Font(pygame.font.get_default_font(), 18)
            text_died = font_died.render("x_x", True, (255, 255, 255))  # Белый цвет для текста "Died"
            text_died_rect = text_died.get_rect(center=(self.x + 40, self.y + 5))

            font_name = pygame.font.Font(pygame.font.get_default_font(), 12)
            text_name = font_name.render(self.name, True, (255, 255, 255))  # Белый цвет для текста с именем
            text_name_rect = text_name.get_rect(center=(self.x + 40, self.y + 25))  # Расположение под надписью "died"

            screen.blit(text_died, text_died_rect.topleft)
            screen.blit(text_name, text_name_rect.topleft)

        elif self.status == 'in_trap':
            self.vel = 0.5


    # -------- CHANGE SIZE
    def change_position(self, position):
        current_time = pygame.time.get_ticks()  # Получает текущее время в миллисекундах.
        time_since_last_change = current_time - self.last_status_change_time  # Вычисляет разницу между текущим временем и временем последнего изменения статуса.

        if time_since_last_change >= self.delay_between_changes:  # прошло достаточно времени?
            if position == "Crouch":
                self.status = "crouch" if self.status != "crouch" else "active"
            else:
                self.status = "active" if self.status != "active" else "crouch"

            self.last_status_change_time = current_time  # Обновляет время последнего изменения статуса

            # Обновление состояние и размеров
            if self.status == "crouch":
                self.vel = 0.5  # скорость
                self.height = 35  # высота
                self.width = 60  # ширина
            else:
                self.vel = 2  # скорость
                self.height = 70  # высота
                self.width = 50  # ширина

            self.update()

    # -------- DRAW COLLISION AREA
    def draw_collision(self, screen):
        collision_surface = pygame.Surface((2 * self.collision_radius, 2 * self.collision_radius), pygame.SRCALPHA)
        pygame.draw.circle(collision_surface, (255, 255, 0, 30 if self.collision_visib else 0),
                           (self.collision_radius, self.collision_radius), self.collision_radius)
        screen.blit(collision_surface, (
        self.x + self.width // 2 - self.collision_radius, self.y + self.height // 2 - self.collision_radius))

    # -------- MOVEMENT
    def move(self, direction):
        if not self.blocked_directions[direction]:
            if direction == "Up":
                self.y -= self.vel
            elif direction == "Left":
                self.x -= self.vel
            elif direction == "Down":
                self.y += self.vel
            elif direction == "Right":
                self.x += self.vel

            self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)