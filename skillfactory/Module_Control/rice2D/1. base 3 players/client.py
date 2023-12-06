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
    p = n.getP()  # Переместите это здесь, чтобы переменная p была определена до использования в цикле
    players = n.send(p)
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        players = n.send(p)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(win, players)

main()
