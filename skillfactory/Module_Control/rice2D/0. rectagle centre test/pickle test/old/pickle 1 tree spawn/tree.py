import pygame

class Tree:
    def __init__(self, x, y, width, height, color, _id):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.id = _id
        self.hp = 2
        self.alive = True
        self.vel = 1

    # ------ TERMINAL DATA
    def __str__(self):
        return f"Tree({self.x}, {self.y}, {self.width}, {self.height}, {self.color}, {self.id})"

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def damage(self):
        self.hp -= 1
        print("Tree :: -1 hp")

    def check_death(self):
        if self.hp <= 0:
            print("Tree destroyed")

    def move(self):
        keys = pygame.key.get_pressed()  # текущее состояние всех клавиш

        if keys[pygame.K_a]:
            self.x -= self.vel
        if keys[pygame.K_d]:
            self.x += self.vel
        if keys[pygame.K_w]:
            self.y -= self.vel
        if keys[pygame.K_s]:
            self.y += self.vel
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
