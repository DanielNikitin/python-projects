import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set the size of the game window
win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))

# Set the title of the game window
pygame.display.set_caption("Top-Down Shooter")

# Set the game FPS
FPS = 60
clock = pygame.time.Clock()

# Set the grid parameters
grid_size = 50
grid_color = (0, 0, 0)

# Set the player parameters
player_color = (0, 255, 0)
player_size = 50
player_rect = pygame.Rect(0, 0, player_size, player_size)
player_rect.center = (win_width // 2, win_height // 2)
player_speed = 10

# Set the bullet parameters
bullet_color = (255, 255, 0)
bullet_size = 10
bullet_rect = pygame.Rect(0, 0, bullet_size, bullet_size)
bullet_rect.center = player_rect.center
bullet_speed = 20
recoil_speed = 10
bullets = []

# Set the enemy parameters
enemy_color = (255, 0, 0)
enemy_size = 50
enemy_speed = 5
enemy_count = 5
enemies = []

# Set the font
font = pygame.font.SysFont("Arial", 24)

# Normalize the vector
def normalize_vector(vector):
    vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if vector_length != 0:
        return vector[0] / vector_length, vector[1] / vector_length
    else:
        return 0, 0


# Define the Bullet class
class Bullet:
    def __init__(self, pos, direction, speed, color):
        self.rect = bullet_rect.copy()
        self.rect.center = pos
        self.direction = direction
        self.speed = speed
        self.color = color

    def move(self):
        self.rect.centerx += self.direction[0] * self.speed
        self.rect.centery += self.direction[1] * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


# Define the Enemy class
class Enemy:
    def __init__(self, pos, size, speed, color):
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = pos
        self.speed = speed
        self.color = color

    def move_towards_player(self, player_rect):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        direction = normalize_vector((dx, dy))
        self.rect.centerx += direction[0] * self.speed
        self.rect.centery += direction[1] * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


# Create the enemies
for i in range(enemy_count):
    x = random.randint(0, 2000)
    y = random.randint(0, 2000)
    enemy = Enemy((x, y), enemy_size, enemy_speed, enemy_color)
    enemies.append(enemy)

# Start the game loop
running = True
while running:
    clock.tick(FPS)
    win.fill("black")
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # Move the player
            keys = pygame.key.get_pressed()
            player_movement = [0, 0]
            if keys[pygame.K_w]:
                player_movement[1] -= player_speed
            if keys[pygame.K_s]:
                player_movement[1] += player_speed
            if keys[pygame.K_a]:
                player_movement[0] -= player_speed
            if keys[pygame.K_d]:
                player_movement[0] += player_speed
            player_rect.move_ip(player_movement)

    # Handle shooting
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = pygame.mouse.get_pos()
        bullet_direction = (mouse_pos[0] - player_rect.centerx, mouse_pos[1] - player_rect.centery)
        bullet_direction = normalize_vector(bullet_direction)
        bullets.append(Bullet(bullet_rect.center, bullet_direction, bullet_speed, bullet_color))

    # Move the bullets
    for bullet in bullets:
        bullet.move()
        # Check for collisions with enemies
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                bullets.remove(bullet)
                break
        # Check for collisions with the edge of the screen
        if not win.get_rect().colliderect(bullet.rect):
            bullets.remove(bullet)

    # Move the enemies
    for enemy in enemies:
        enemy.move_towards_player(player_rect)

    # Draw the grid
    for x in range(0, win_width, grid_size):
        pygame.draw.line(win, grid_color, (x, 0), (x, win_height))
    for y in range(0, win_height, grid_size):
        pygame.draw.line(win, grid_color, (0, y), (win_width, y))

    # Draw the player
    pygame.draw.rect(win, player_color, player_rect)

    # Draw the bullets
    for bullet in bullets:
        bullet.draw(win)

    # Draw the enemies
    for enemy in enemies:
        enemy.draw(win)

    pygame.display.update()
pygame.quit()
