import pygame

def info_hud(screen, info_data):
    width = 5
    height = 5

    font = pygame.font.SysFont('calibri', 20)
    info_text = f"{info_data['info_data']}"
    text = font.render(info_text, True, (255, 255, 255))
    screen.blit(text, (width, height))

def other_hud(screen, other_data):
    width = 5
    height = 25

    font = pygame.font.SysFont('calibri', 20)
    other_text = f"VEL: {other_data['other_data']}"
    text = font.render(other_text, True, (255, 255, 255))
    screen.blit(text, (width, height))

def hp_hud(screen, hp_data):
    width = 5
    height = 45

    font = pygame.font.SysFont('calibri', 20)
    hp_text = f"HP: {hp_data['hp_data']}"
    text = font.render(hp_text, True, (255, 255, 255))
    screen.blit(text, (width, height))

def draw_fps(screen, fps):
    width = 400
    height = 5

    font = pygame.font.SysFont('calibri', 20)
    fps_text = f"FPS: {fps:.2f}"
    text = font.render(fps_text, True, (255, 255, 255))
    screen.blit(text, (width, height))

def draw_huds(screen, info_data, other_data, hp_data, fps):
    info_hud(screen, info_data)
    other_hud(screen, other_data)
    hp_hud(screen, hp_data)
    draw_fps(screen, fps)
