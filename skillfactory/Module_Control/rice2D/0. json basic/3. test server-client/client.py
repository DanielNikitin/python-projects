import socket
import pygame
import json

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Client")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

welcome_message_received = False
game_state = {'player_pos': (50, 50)}

def redraw_window(screen, player_pos, welcome_text):
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], 50, 50))

    font = pygame.font.Font(None, 36)
    text = font.render(welcome_text, True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()

    message = {'action': 'move', 'data': mouse_pos}
    client.send(json.dumps(message).encode('utf-8'))

    try:
        data = client.recv(1024).decode('utf-8')
        if data:
            try:
                data_json = json.loads(data)

                if 'action' in data_json and data_json['action'] == 'welcome' and not welcome_message_received:
                    welcome_text = data_json['data']
                    welcome_message_received = True
                elif 'player_pos' in data_json:
                    game_state = data_json
            except json.JSONDecodeError:
                pass
    except ConnectionResetError:
        print("Server closed the connection.")
        running = False

    redraw_window(screen, game_state['player_pos'], welcome_text=welcome_text)

    clock.tick(60)

pygame.quit()
client.close()
