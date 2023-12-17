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
    print(f"P: {p}")

    try:
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            players = n.send(p)
            print(f"N.SEND(P) :: {n.send(p)}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            p.move()
            redrawWindow(screen, players)

    except Exception as e:
        print(f"Client Error :: {e}")

main()
