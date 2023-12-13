import pygame
import pickle

from network import Network

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client 1")


def redrawWindow(screen, trees):  # рисуем деревья
    screen.fill('gray25')

    try:
        for tree in trees:  # находим дерево в списке деревьев
            tree.draw(screen)  # отображаем его в игровом мире клиента

    except Exception as se:
        print(f"redrawWindow :: {se}")

    pygame.display.update()  # обновляем состояние экрана


def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()

    try:
        while run:
            clock.tick(60)

            received_data = n.get_data()  # Получить данные
            loaded_data = pickle.loads(received_data)
            print(loaded_data)

            # Extract trees and ores using the get method
            #trees = loaded_data.get("trees", [])
            #print(f"trees_data: {trees}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            redrawWindow(screen, trees)  # Рисовать новое состояние деревьев

    except Exception as e:
        print(f"main :: {e}")
    finally:
        pygame.quit()


main()