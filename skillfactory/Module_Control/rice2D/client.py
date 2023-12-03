import pygame
from network import Network
from player import Player

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, players):
    win.fill((255, 255, 255))
    for player in players:
        player.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    player = n.getP()  # Используйте player вместо p
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        players = n.send(player)  # Получайте список всех игроков

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        player.move()
        redrawWindow(win, players)

main()