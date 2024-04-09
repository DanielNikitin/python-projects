import pygame
import json
import time

from network import Network

pygame.init()

# Определение размеров экрана
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Создание игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Client")

clock = pygame.time.Clock()

def draw_window():
    screen.fill((0, 0, 0))

    pygame.display.flip()
    clock.tick(60)


def main():
    run = True
    network = Network()
    network.connect()

    try:
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # -------- DATA TO SEND
            network.send_data({"action": "move_right"})

            # -------- RECEIVED DATA
            received_data = network.receive_data()

            if received_data is not None:
                print(received_data)

        draw_window()
    except KeyboardInterrupt:
        pass
    finally:
        network.disconnect()


main()