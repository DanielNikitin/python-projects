import pygame

# если мы подключаем библиотеку network, она автоматически начинает работать
from network import Network
from tree import Tree
from ore import Ore

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client 2")


def redrawWindow(screen, trees, ores):  # рисуем деревья
    screen.fill('gray25')

    try:
        for tree in trees:
            tree.draw(screen)

        for ore in ores:
            ore.draw(screen)

    except Exception as se:
        print(f"for tree in trees :: {se}")

    pygame.display.update()  # обновляем состояние экрана


def main():
    run = True
    n = Network()

    clock = pygame.time.Clock()

    try:

        while run:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        n.send('r')

            # Получаем данные об деревьях в списке деревьев и ничего более
            #trees = n.get_data()

            # Получаем и обновляем состояние деревьев
            objects = n.send_and_rec('')
            trees, ores = objects

            redrawWindow(screen, trees, ores)  # обновляем экран

    except Exception as e:
        print(f"main :: {e}")
    finally:
        pygame.quit()


main()