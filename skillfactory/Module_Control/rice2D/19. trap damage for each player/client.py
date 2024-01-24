import pygame
import time

from network import Network
from hud import *
from keys import *

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

pygame.init()
clock = pygame.time.Clock()

def redrawWindow(players, trees, ores, traps,
                 info_data, other_data, hp_data,
                 fps):

    screen.fill('gray25')

    for player in players:
        player.draw(screen)
        draw_huds(screen, info_data, other_data, hp_data, fps)

    for tree in trees:
        tree.draw(screen)

    for ore in ores:
        ore.draw(screen)

    for trap in traps:
        trap.draw(screen)

    pygame.display.update()


def main():
    run = True

    server = Network()
    conn_status = server.connect()

    try:
        while run:
            clock.tick(120)
            fps = clock.get_fps()

            data = server.send({"": conn_status})  # send and reply

            if data is not None:
                (players, trees, ores, traps,
                 info_data, other_data, hp_data) = data

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()

                # -------- HANDLE KEYS
                client_up, client_left, client_down, client_right, client_crouch = handle_keys()

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
                    server.send({"client_action": "mode", "position": "Crouch"})  # C

                redrawWindow(players, trees, ores, traps,
                             info_data, other_data, hp_data, fps)

    except Exception as e:
        server.disconnect()
        print(f"Client Error :: {e}")


main()