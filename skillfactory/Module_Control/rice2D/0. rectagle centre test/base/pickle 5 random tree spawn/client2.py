import pygame

# если мы подключаем библиотеку network, она автоматически начинает работать
from network import Network
from tree import Tree

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client 2")


def redrawWindow(screen, trees):  # рисуем деревья
    screen.fill('gray25')

    try:
        for tree in trees:  # находим дерево в списке деревьев
            tree.draw(screen)  # отображаем его в игровом мире клиента

    except Exception as se:
        print(f"for tree in trees :: {se}")

    pygame.display.update()  # обновляем состояние экрана


def main():
    run = True

    n = Network()

    # Получаем данные об деревьях в списке деревьев
    tree = n.get_data()

    clock = pygame.time.Clock()

    try:

        while run:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            redrawWindow(screen, tree)  # рисуем новое состояние дерева

    except Exception as e:
        print(f"main :: {e}")
    finally:
        pygame.quit()


main()