import pygame

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
