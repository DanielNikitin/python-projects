import pygame

# если мы подключаем библиотеку network, она автоматически начинает работать
from network import *
from three import *

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client 1")


def redrawWindow(screen, threes):  # рисуем деревья
    screen.fill('gray25')

    try:
        for three in threes:  # находим дерево в списке деревьев
            three[0].draw(screen)  # отображаем его в игровом мире клиента
    except Exception as se:
        print(f"for three in threes :: {se}")

    pygame.display.update()  # обновляем состояние экрана


def main():
    run = True

    n = Network()
    t = n.get_data()  # получаем данные про дерево

    try:
        clock = pygame.time.Clock()
        while run:

            clock.tick(60)

            three_data = n.send(t)
            three = Three.from_dict(three_data)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            redrawWindow(screen, [three])  # рисуем новое состояние дерева

    except Exception as e:
        print(f"main :: {e}")
    finally:
        pygame.quit()


main()