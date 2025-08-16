import pygame
from network import Network

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

pygame.init()

def redrawWindow(screen, players, trees, ores, extra_data):
    screen.fill('gray25')

    for player in players:
        player.draw(screen)

    for tree in trees:
        tree.draw(screen)

    for ore in ores:
        ore.draw(screen)

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
    client_crouch = False  # C

    try:
        clock = pygame.time.Clock()
        while run:
            clock.tick(120)
            data = server.send({"player": status})

            if data is not None:
                players, trees, ores, extra_data = data
                #print(f"GET DATA :: {data}")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()

                    # -------- KEYDOWN
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:  # W
                            print("w is pressed")
                            client_up = True
                        if event.key == pygame.K_a:  # A
                            print("a is pressed")
                            client_left = True
                        if event.key == pygame.K_s:  # S
                            print("s is pressed")
                            client_down = True
                        if event.key == pygame.K_d:  # D
                            print("d is pressed")
                            client_right = True
                        if event.key == pygame.K_c:  # C
                            print("c is pressed")
                            client_crouch = True

                        if event.key == pygame.K_g:
                            print('change_text')
                            server.send({"client_hud": "change_text"})


                    # -------- KEYUP
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_w:  # W
                            print("w is unpressed")
                            client_up = False
                        if event.key == pygame.K_a:  # A
                            print("a is unpressed")
                            client_left = False
                        if event.key == pygame.K_s:  # S
                            print("s is unpressed")
                            client_down = False
                        if event.key == pygame.K_d:  # D
                            print("d is unpressed")
                            client_right = False
                        if event.key == pygame.K_c:  # C
                            print("c is unpressed")
                            client_crouch = False

                # -------- SENDING TO SERVER
                if client_up:
                    server.send({"client_action": "move", "direction": "Up"})  # W
                if client_left:
                    server.send({"client_action": "move", "direction": "Left"})  # A
                if client_down:
                    server.send({"client_action": "move", "direction": "Down"})  # S
                if client_right:
                    server.send({"client_action": "move", "direction": "Right"})  # D
                if client_crouch:
                    server.send({"client_action": "status", "position": "Crouch"})  # C

                redrawWindow(screen, players, trees, ores, extra_data)

    except Exception as e:
        print(f"Client Error :: {e}")

main()