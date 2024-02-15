import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры экрана
width = 500
height = 500

# Цвета
black = (0, 0, 0)
blue = (0, 0, 255)

# Создание экрана
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blue rectangle")

# Создание прямоугольника
rect_width = 50
rect_height = 70
rect_x = (width - rect_width) // 2
rect_y = (height - rect_height) // 2
player_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

# Основной цикл программы
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Очистка экрана
    screen.fill(black)

    # Рисование прямоугольника
    pygame.draw.rect(screen, blue, player_rect)

    # Обновление экрана
    pygame.display.flip()

    # Задержка для управления частотой обновления
    pygame.time.delay(10)

# Завершение работы Pygame
pygame.quit()
sys.exit()
