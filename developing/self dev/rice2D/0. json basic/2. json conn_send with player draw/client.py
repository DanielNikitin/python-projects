import pygame
from network import Network

pygame.init()

# Определение размеров экрана
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Создание игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Client")

clock = pygame.time.Clock()

# Цвета
black = (0, 0, 0)
blue = (0, 0, 255)


def draw_window(screen, blue, player_rect):
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, blue, player_rect)

    pygame.display.flip()
    clock.tick(60)


def main():
    run = True
    network = Network()
    network.connect()

    # Инициализация player_rect перед циклом
    rect_width = 50
    rect_height = 70
    rect_x = (SCREEN_WIDTH - rect_width) // 2
    rect_y = (SCREEN_HEIGHT - rect_height) // 2
    player_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    try:
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # -------- DATA TO SEND
            network.send_data({"action": "move_right"})

            # -------- RECEIVED DATA
            received_data = network.receive_data()

            if received_data is not None:
                print(received_data)

            draw_window(screen, blue, player_rect)
    except KeyboardInterrupt:
        pass
    finally:
        network.disconnect()


if __name__ == "__main__":
    main()
