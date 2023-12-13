# CLIENT

from client_network import Network
from client_config import *

pygame.init()  # инициализация игры

def redraw_window(screen, players):
    screen.fill('gray25')

    for player in players:
        player.draw()

    pygame.display.update()


def client_connect():
    run = True
    try:
        clock = pygame.time.Clock()

        n = Network()
        from_server = n.get_server_data()

        players = from_server.get('players', [])
        print(players)

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            #redraw_window(screen, players)

    except Exception as e:
        print(f"Client Error :: {e}")

client_connect()