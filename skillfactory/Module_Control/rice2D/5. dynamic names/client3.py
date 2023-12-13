import pygame
from network import Network

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

pygame.init()  # инициализация игры


def redrawWindow(screen, players):
    screen.fill('gray25')
    for player in players:
        player.draw(screen)
    pygame.display.update()


def main():
    run = True
    n = Network()  # обращаемся к client_network.py (связующий)
    p = n.getP()  # обращаемся к Player из player.py а так же соединяемся с сервером

    try:
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            players = n.send(p)  # отправляет данные о состоянии игрока серверу и получаем данные от сервера
            print(n.send(p))

            for event in pygame.event.get():  # отслеживаем события
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            p.move()  #  через client_network.py мы можем обратиться к player.py и выполнить функцию move
            redrawWindow(screen, players)

    except Exception as e:
        print(f"Client Error :: {e}")

main()
