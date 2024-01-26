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
