# keys.py
import pygame

def handle_keys():
    keys = pygame.key.get_pressed()

    client_up = keys[pygame.K_w]
    client_left = keys[pygame.K_a]
    client_down = keys[pygame.K_s]
    client_right = keys[pygame.K_d]
    client_crouch = keys[pygame.K_c]

    return client_up, client_left, client_down, client_right, client_crouch


# -------- HANDLE KEYS
client_up, client_left, client_down, client_right, client_crouch = handle_keys()

# -------- SENDING TO SERVER
if client_up:
    network.send_data({"action": "move_up"})  # W
    print("w")
if client_left:
    network.send_data({"action": "move_left"})  # A
    print("a")
if client_down:
    network.send_data({"action": "move_down"})  # S
    print("s")
if client_right:
    network.send_data({"action": "move_right"})  # D
    print("d")
if client_crouch:
    network.send_data({"mode": "crouch"})  # C
    print("c")