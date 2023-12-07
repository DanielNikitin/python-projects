import pygame
from network import Network

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

pygame.init()  # инициализация игры


def redrawWindow(screen, players, cubes):
    screen.fill('gray25')
    for player in players:
        player.draw(screen)

    for cube in cubes:
        cube.draw(screen)

    pygame.display.update()


def main():
    run = True
    n = Network()  # обращаемся к network.py (связующий)
    p = n.getP()

    try:
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            players, cubes = n.send((p, p))


            for event in pygame.event.get():  # отслеживаем события
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            p.move()  #  через network.py мы можем обратиться к player.py и выполнить функцию move
            p.change_size()

            redrawWindow(screen, players, cubes)

    except Exception as e:
        print(f"Client Error :: {e}")

main()
