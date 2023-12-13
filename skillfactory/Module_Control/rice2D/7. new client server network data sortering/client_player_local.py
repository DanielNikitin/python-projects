# CLIENT

from client_network import Network
from client_config import *

from player import Player

pygame.init()  # инициализация игры

def redraw_window(screen, player):
    screen.fill('gray25')
    player.draw(screen)
    pygame.display.update()


def client_connect():
    run = True
    try:
        clock = pygame.time.Clock()

        #n = Network()
        #from_server = n.get_server_data()

        p = Player(50, 50, 100, 100, (0, 144, 0), 'Cock', 1)

        while run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            p.move()
            redraw_window(screen, p)

    except Exception as e:
        print(f"Client Error :: {e}")

client_connect()