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
    n = Network()
    p = n.getP()

    try:
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            data = n.send({"player": p})

            if data is not None:
                players, trees, ores, extra_data = data

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                        print('tree_delete')
                        n.send({"player": p, "p_action": "tree_delete"})

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                        print('change_text')
                        n.send({"player": p, "p_action": "change_text"})

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                        print('receive_damage')
                        p.receive_damage()

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                        print('l')


                p.move()
                p.change_size()

                redrawWindow(screen, players, trees, ores, extra_data)

    except Exception as e:
        print(f"Client Error :: {e}")

main()
