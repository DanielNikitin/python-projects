import pygame
import pickle

# если мы подключаем библиотеку network, она автоматически начинает работать
from network import Network

from player import Player
from tree import Tree
from ore import Ore

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client 1")


def redrawWindow(screen, players, trees, ores):  # рисуем деревья
    screen.fill('gray25')

    try:

        for player in players:
            player.draw(screen)

        for tree in trees:
            tree.draw(screen)

        for ore in ores:
            ore.draw(screen)

    except Exception as se:
        print(f"redrawWindow :: {se}")

    pygame.display.update()  # обновляем состояние экрана


def main():
    run = True
    clock = pygame.time.Clock()

    n = Network()
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


            trees = n.get_data()
            ores = n.get_data()
            players = n.get_data()

            redrawWindow(screen, players, trees, ores)  # обновляем экран

    except Exception as e:
        print(f"main :: {e}")
    finally:
        pygame.quit()


main()