# ----Client----

import socket
import pygame
#import time

#----НАСТРОЙКИ ОКНА----
WIDTH_WINDOW, HEIGHT_WINDOW = 1000, 800
#-----------------------

#--СОЗДАНИЕ ОКНА ИГРЫ--
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
pygame.display.set_caption('fastDik prodaction')
#-----------------------

print('CLIENT: ПРОБУЕМ ПОДКЛЮЧИТСЯ')

#----СОЗДАНИЕ СОКЕТА----
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 10000))
#-----------------------

data_received = False

client_running = True
while client_running:

    #--ОБРАБОТКА СОБЫТИЙ В ОКНЕ КЛИЕНТА--
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            client_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print('key 1 pushed')
    #-----------------------------

    #--ПОЛУЧАЕМ ОТ СЕРВЕРА СОСТОЯНИЕ ИГРЫ--
    try:
        data = sock.recv(1024)
        data = data.decode()
        if not data:
            print('Сервер выключился')
            break
    except:
        print('CLIENT: Ошибка при получении данных от сервера')
        break

    #--ПОЛУЧАЕМ ОТ СЕРВЕРА СОСТОЯНИЕ ПОДКЛЮЧЕНИЯ--
    if data.startswith("SERVER:"):
        print(data)
        if not data_received:
            print('CLIENT: Не удалось подключится к серверу')
            data_received = True

    #----КООРДИНАТЫ КУРСОРА----
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        v = (pos[0] - WIDTH_WINDOW//2, pos[1]-HEIGHT_WINDOW//2)

    #--ОТПРАВЛЯЕМ_КОМАНДУ_СЕРВЕРУ--
    message = '-,..,-'
    sock.send(message.encode())
    #----------------------------

    #--ОТОБРАЖАЕМ_СОСТОЯНИЕ_ИГРЫ-
    screen.fill('grey25')
    #print(data)
    #----------------------------

    #pygame.draw.circle(screen, colors[self.color],
     #                  (WIDTH_WINDOW // 2, HEIGHT_WINDOW / 2), self.r)
    # (где, цвет, координаты, радиус, ширина)

    pygame.display.flip()

pygame.quit()  # закрываем окно
print('Окно закрыто')