import pygame

pygame.init()

# Определение размеров экрана
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

new_width = 250
new_height = 250

# Создание игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Anim Test")

# Загрузка спрайтов "idle"
sprites_idle_up = [pygame.image.load("sprites/idle/iu1.png"),
                   pygame.image.load("sprites/idle/iu2.png"),
                   pygame.image.load("sprites/idle/iu3.png"),
                   pygame.image.load("sprites/idle/iu4.png")]

sprites_idle_left = [pygame.image.load("sprites/idle/il1.png"),
                     pygame.image.load("sprites/idle/il2.png"),
                     pygame.image.load("sprites/idle/il3.png"),
                     pygame.image.load("sprites/idle/il4.png")]

sprites_idle_right = [pygame.image.load("sprites/idle/ir1.png"),
                      pygame.image.load("sprites/idle/ir2.png"),
                      pygame.image.load("sprites/idle/ir3.png"),
                      pygame.image.load("sprites/idle/ir4.png")]

sprites_idle_down = [pygame.image.load("sprites/idle/id1.png"),
                     pygame.image.load("sprites/idle/id2.png"),
                     pygame.image.load("sprites/idle/id3.png"),
                     pygame.image.load("sprites/idle/id4.png")]

# Загрузка спрайтов "move"
sprites_up = [pygame.image.load("sprites/walk/wu1.png"),
              pygame.image.load("sprites/walk/wu2.png"),
              pygame.image.load("sprites/walk/wu3.png"),
              pygame.image.load("sprites/walk/wu4.png")]

sprites_left = [pygame.image.load("sprites/walk/wl1.png"),
                pygame.image.load("sprites/walk/wl2.png"),
                pygame.image.load("sprites/walk/wl3.png"),
                pygame.image.load("sprites/walk/wl4.png")]

sprites_right = [pygame.image.load("sprites/walk/wr1.png"),
                 pygame.image.load("sprites/walk/wr2.png"),
                 pygame.image.load("sprites/walk/wr3.png"),
                 pygame.image.load("sprites/walk/wr4.png")]

sprites_down = [pygame.image.load("sprites/walk/wd1.png"),
                pygame.image.load("sprites/walk/wd2.png"),
                pygame.image.load("sprites/walk/wd3.png"),
                pygame.image.load("sprites/walk/wd4.png")]

# Пример изменения размеров для спрайтов "idle"
scaled_sprites_idle_up = [pygame.transform.scale(sprite, (new_width, new_height)) for sprite in sprites_idle_up]
scaled_sprites_idle_left = [pygame.transform.scale(sprite, (new_width, new_height)) for sprite in sprites_idle_left]
scaled_sprites_idle_right = [pygame.transform.scale(sprite, (new_width, new_height)) for sprite in sprites_idle_right]
scaled_sprites_idle_down = [pygame.transform.scale(sprite, (new_width, new_height)) for sprite in sprites_idle_down]

# Пример изменения размеров для спрайтов "move"
scaled_sprites_up = [pygame.transform.scale(sprite, (new_width, new_height)) for sprite in sprites_up]
scaled_sprites_left = [pygame.transform.scale(sprite, (new_width, new_height)) for sprite in sprites_left]
scaled_sprites_right = [pygame.transform.scale(sprite, (new_width, new_height)) for sprite in sprites_right]
scaled_sprites_down = [pygame.transform.scale(sprite, (new_width, new_height)) for sprite in sprites_down]

background_image = pygame.image.load("bg.png")
background_rect = background_image.get_rect(center=[SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])

sprite_rect = scaled_sprites_right[0].get_rect()  # Используйте отмасштабированный спрайт
sprite_rect.x = 299
sprite_rect.y = 209

speed = 3
frame_rate = 10

background_x = 0
background_y = 0

current_frame = 0

clock = pygame.time.Clock()

running = True
is_idle = False
last_direction = "down"
current_sprites = scaled_sprites_idle_down  # Используйте отмасштабированный спрайт

def get_idle_sprites(direction):
    if direction == "up":
        return scaled_sprites_idle_up
    elif direction == "left":
        return scaled_sprites_idle_left
    elif direction == "right":
        return scaled_sprites_idle_right
    elif direction == "down":
        return scaled_sprites_idle_down

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        last_direction = "up"
        is_idle = False
        current_sprites = scaled_sprites_up
        current_frame += 0.2
        background_y += speed
    elif keys[pygame.K_a]:
        last_direction = "left"
        is_idle = False
        current_sprites = scaled_sprites_left
        current_frame += 0.2
        background_x += speed
    elif keys[pygame.K_d]:
        last_direction = "right"
        is_idle = False
        current_sprites = scaled_sprites_right
        current_frame += 0.2
        background_x -= speed
    elif keys[pygame.K_s]:
        last_direction = "down"
        is_idle = False
        current_sprites = scaled_sprites_down
        current_frame += 0.2
        background_y -= speed
    else:
        is_idle = True
        current_frame += 0.2

    if is_idle:
        current_sprites = get_idle_sprites(last_direction)

    if current_frame >= len(current_sprites):
        current_frame = 0
    if current_frame == 4:
        current_frame = 0

    screen.fill((0, 0, 0))
    screen.blit(background_image, (background_x, background_y))
    screen.blit(current_sprites[int(current_frame)], sprite_rect)

    pygame.display.flip()
    clock.tick(60)
