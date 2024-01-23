import pygame

def info_hud(screen, info_data):
    width = 5
    height = 5

    font = pygame.font.SysFont('calibri', 20)
    text = font.render(info_data["info_data"], True, (255, 255, 255))
    screen.blit(text, (width, height))

def other_hud(screen, other_data):
    width = 5
    height = 25

    font = pygame.font.SysFont('calibri', 20)
    text = font.render(other_data["other_data"], True, (255, 255, 255))
    screen.blit(text, (width, height))

def hp_hud(screen, hp_data):
    width = 5
    height = 45

    font = pygame.font.SysFont('calibri', 20)
    text = font.render(hp_data["hp_data"], True, (255, 255, 255))
    screen.blit(text, (width, height))

def draw_huds(screen, info_data, other_data, hp_data):
    info_hud(screen, info_data)
    other_hud(screen, other_data)
    hp_hud(screen, hp_data)
