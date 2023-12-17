# CLIENT

from client_network import Network
from client_config import *

pygame.init()  # инициализация игры

def redraw_window(screen, players):
    screen.fill('gray25')

    for player in players:
        player.draw(screen)

    pygame.display.update()


def client_connect():
    run = True

    try:
        clock = pygame.time.Clock()

        n = Network()

        # LOAD DATA
        from_server = n.get_server_data()

        player = from_server.get('player', {})
        print(f"FROM SERVER :: PLAYER: {player}")

        while run:
            clock.tick(60)

            # LOAD DATA
            players = from_server.get('players_list', {})
            print(f"FROM SERVER :: PLAYERS LIST: {players}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

            player.move()

            # SEND DATA
            n.send_data({'players_list': player})

            # UPDATE CLIENT SCREEN
            redraw_window(screen, players)

    except Exception as e:
        print(f"Client Error :: {e}")

client_connect()