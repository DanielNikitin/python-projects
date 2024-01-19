import pygame
from network import Network

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

pygame.init()

def redrawWindow(screen, players, extra_data):
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

# -------- CLIENT KEY CONDITIONS
    client_up = False  # W
    client_left = False  # A
    client_down = False  # S
    client_right = False  # D

    try:
        clock = pygame.time.Clock()
        while run:
            clock.tick(120)
            data = server.send({"player": status})

            if data is not None:
                players, extra_data = data
                #print(f"GET DATA :: {data}")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()

                    # -------- KEYDOWN
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            print("w is pressed")
                            client_up = True
                        if event.key == pygame.K_a:
                            print("a is pressed")
                            client_left = True
                        if event.key == pygame.K_s:
                            print("s is pressed")
                            client_down = True
                        if event.key == pygame.K_d:
                            print("d is pressed")
                            client_right = True

                        if event.key == pygame.K_g:
                            print('change_text')
                            server.send({"client_hud": "change_text"})


                    # -------- KEYUP
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:
                            print("w is pressed")
                            client_up = False
                        if event.key == pygame.K_a:
                            print("a is pressed")
                            client_left = False
                        if event.key == pygame.K_s:
                            print("s is pressed")
                            client_down = False
                        if event.key == pygame.K_d:
                            print("d is pressed")
                            client_right = False

                # -------- SENDING TO SERVER
                if client_up:
                    server.send({"action": "move", "direction": "Up"})  # W
                if client_left:
                    server.send({"action": "move", "direction": "Left"})  # A
                if client_down:
                    server.send({"action": "move", "direction": "Down"})  # S
                if client_right:
                    server.send({"action": "move", "direction": "Right"})  # D

                redrawWindow(screen, players, extra_data)

    except Exception as e:
        print(f"Client Error :: {e}")

main()