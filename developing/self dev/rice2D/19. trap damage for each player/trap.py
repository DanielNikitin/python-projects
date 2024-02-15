import pygame
import time

class Trap:
    def __init__(self, x, y, width, height, color, _id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.id = _id

        self.collision_radius = 20
        self.collision_visib = True

        self.status = False

        self.damage_timer = pygame.time.get_ticks()

    # ------ TERMINAL DATA
    def __str__(self):
        return f"Trap({self.x}, {self.y}, {self.width}, {self.height}, {self.color}, {self.id})"

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.draw_collision(screen)  # collision area

    # -------- DRAW COLLISION AREA
    def draw_collision(self, screen):
        collision_surface = pygame.Surface((2 * self.collision_radius, 2 * self.collision_radius), pygame.SRCALPHA)
        pygame.draw.circle(collision_surface, (255, 255, 0, 32 if self.collision_visib else 0),
                           (self.collision_radius, self.collision_radius), self.collision_radius)
        screen.blit(collision_surface, (
        self.x + self.width // 2 - self.collision_radius, self.y + self.height // 2 - self.collision_radius))

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def apply_damage(self, player_data):
        damage_interval = 300  # Интервал урона в миллисекундах (1000 = 1 секунда)

        # Проверка таймера для урона
        if self.status and pygame.time.get_ticks() - self.damage_timer >= damage_interval:
            player_data.hp -= 1
            player_data.vel = 0.5
            self.damage_timer = pygame.time.get_ticks()  # Сбрасываем таймер урона
