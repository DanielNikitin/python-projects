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
        self.vel = 3

        self.hp = hp
        self.collision_radius = 50

        self.name = name
        self.id = _id

        self.status = "active"

        self.last_status_change_time = 0
        self.delay_between_changes = 1000  # Задержка в миллисекундах (в данном случае 1 секунда)


    # ------ TERMINAL DATA
    def __str__(self):
        return f"Player({self.x}, {self.y}, {self.width}, {self.height}, {self.color}, {self.name}, {self.id})"


    def draw(self, screen):
        # Отрисовываем health bar
        self.draw_health_bar(screen)
        self.draw_collision(screen)

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


    def change_size(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_h]:
            current_time = pygame.time.get_ticks()  # Получает текущее время в миллисекундах.
            time_since_last_change = current_time - self.last_status_change_time  # Вычисляет разницу между текущим временем и временем последнего изменения статуса.

            if time_since_last_change >= self.delay_between_changes:  # прошло достаточно времени?

                if self.status == "active":
                    self.status = "crouch"
                else:
                    self.status = "active"
                self.last_status_change_time = current_time  # Обновляет время последнего изменения статуса

                # Установка скорости в зависимости от статуса
                if self.status == "crouch":
                    self.vel = 1
                else:
                    self.vel = 3

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

    def draw_collision(self, screen):
        pygame.draw.circle(screen, (255, 255, 0, 128), (self.x + self.width // 2, self.y + self.height // 2),
                           self.collision_radius, 2)

    def receive_damage(self):
        if self.hp > 0:
            self.hp -= 1
            print(f"{self.name} получил урон. Текущее здоровье: {self.hp}")
            self.update()
        else:
            print(f"{self.name} уже мертв.")

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

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
