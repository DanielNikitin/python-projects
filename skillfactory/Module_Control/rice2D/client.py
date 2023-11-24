import pygame

width = 800
height = 800
c_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)  # checking character collision or something like that
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.vel

        if keys[pygame.K_d]:
            self.x += self.vel

        if keys[pygame.K_w]:
            self.y -= self.vel

        if keys[pygame.K_s]:
            self.y += self.vel

        self.rect = (self.x, self.y, self.width, self.height)  # for update player move


def redrawWindow(c_window, player):
    c_window.fill((255,255,255))
    player.draw(c_window)
    pygame.display.update()


def main():
    run = True
    p = Player(100, 100, 100, 100, (0,255,0))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(c_window, p)

main()