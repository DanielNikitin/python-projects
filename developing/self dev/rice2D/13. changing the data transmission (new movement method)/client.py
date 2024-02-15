import pygame
from network import Network

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

pygame.init()

def redrawWindow(players, extra_data):
    screen.fill('gray25')

    for player in players:
        player.draw(screen)

    font = pygame.font.SysFont('calibri', 20)
    text = font.render(extra_data["message"], True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.update()

def main():
    run = True

    server = Network()
    status = server.connect()

    try:
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            data = server.send({"player": status})

            if data is not None:
                players, extra_data = data
                print(f"GET DATA :: {data}")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_d:
                            print("D")
                            server.send({"action": "move", "direction": "Right"})

                        elif event.key == pygame.K_g:
                            print('change_text')
                            server.send("change_text")


                redrawWindow(players, extra_data)

    except Exception as e:
        print(f"Client Error :: {e}")

main()