import pygame
#import random
import time


class Player:
    def __init__(self, x, y, width, height, color, name, _id, hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.name = name
        self.id = _id
        self.vel = 1.5  # character speed

        self.hp = hp

        self.collision_radius = 50
        self.collision_visib = True  # in dev

        self.status = "active"

        # -------- CROUCH CONSTANT
        self.last_status_change_time = 0
        self.delay_between_changes = 300  # Задержка в миллисекундах (в данном случае 0.3 секунды)

        self.blocked_directions = {"Up": False, "Left": False, "Down": False, "Right": False}

    # -------- TERMINAL DATA
    def __str__(self):
        return f"Player({self.x}, {self.y}, {self.width}, {self.height}, {self.color}, {self.name}, {self.id})"

    # -------- DRAW
    def draw(self, screen):

        self.draw_health_bar(screen)  # health bar
        self.draw_collision(screen)  # collision area

        font = pygame.font.Font(pygame.font.get_default_font(), 20)  # Размер шрифта для никнейма

        if self.status == "sleep":
            # Если статус "sleep", рисуем горизонтальный прямоугольник 60, 35
            pygame.draw.rect(screen, self.color, (self.x, self.y, 60, 35))

            font_sleep = pygame.font.Font(pygame.font.get_default_font(), 15)  # Уменьшили размер шрифта для (sleep)
            text_sleep = font_sleep.render("(sleep)", True, (0, 0, 0))  # 0,0,0 - black color
            text_name = font.render(f"{self.name}", True, (0, 0, 0))  # 0,0,0 - black color

            text_sleep_rect = text_sleep.get_rect(center=(self.x + 30, self.y + 45))  # Центруем надпись (sleep)
            text_name_rect = text_name.get_rect(center=(self.x + 25, self.y + 17.5))  # Центруем надпись с именем

            screen.blit(text_sleep, text_sleep_rect.topleft)
            screen.blit(text_name, text_name_rect.topleft)

        elif self.status == 'active':
            # В противном случае рисуем текущий прямоугольник с размерами
            pygame.draw.rect(screen, self.color, self.rect)

            text = font.render(self.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + 25, self.y + 17.5))  # Центрируем надпись с именем

            screen.blit(text, text_rect.topleft)

        elif self.status == 'crouch':
            pygame.draw.rect(screen, self.color, (self.x, self.y, 60, 35))

            text = font.render(self.name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + 25, self.y + 17.5))  # Центрируем надпись с именем

            screen.blit(text, text_rect.topleft)

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
                self.vel = 1.5  # скорость
                self.height = 70  # высота
                self.width = 50  # ширина

            self.update()

    # -------- DRAW HEALTH BAR
    def draw_health_bar(self, screen):
        bar_width = 50  # ширина
        bar_height = 5  # высота
        bar_x = self.x + (self.width - bar_width) / 2  # X левого верхнего угла
        bar_y = self.y - 7  # Y левого верхнего угла

        # Отрисовываем темно-красный задний фон health bar
        background_color = (100, 0, 0)  # Темно-красный цвет для заднего фона
        pygame.draw.rect(screen, background_color, (bar_x, bar_y, bar_width, bar_height))

        # Вычисляем ширину health bar в зависимости от текущего здоровья
        health_width = int((self.hp / 10) * bar_width)
        health_color = (255, 0, 0)  # Красный цвет для полосы здоровья
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))

    # -------- DRAW COLLISION AREA
    def draw_collision(self, screen):
        collision_surface = pygame.Surface((2 * self.collision_radius, 2 * self.collision_radius), pygame.SRCALPHA)
        pygame.draw.circle(collision_surface, (255, 255, 0, 30 if self.collision_visib else 0),
                           (self.collision_radius, self.collision_radius), self.collision_radius)
        screen.blit(collision_surface, (
        self.x + self.width // 2 - self.collision_radius, self.y + self.height // 2 - self.collision_radius))

    # -------- RECEIVE DAMAGE
    def receive_damage(self):
        if self.hp > 0:
            self.hp -= 1
            print(f"{self.name} получил урон. Текущее здоровье: {self.hp}")
            self.update()
        else:
            print(f"{self.name} уже мертв.")

        for tree in tree_list:
            if is_rect_collision(test_player, tree, hard_collision=True):
                return True

        for ore in ore_list:
            if is_rect_collision(test_player, ore, hard_collision=True):
                return True

        return False

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