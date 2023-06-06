# ----Server----


import socket
import pygame
#import random

#--НАСТРОЙКИ СЕРВЕРА--
server_ip = 'localhost'
FPS = 60  # server speed

WIDHT_WORLD, HEIGHT_WORLD = 4000, 4000  # Размер мира
WIDHT_SERVER_WINDOW, HEIGHT_SERVER_ROOM = 300, 300  # Серверное окно
#-------------------

pygame.init()  # запуск pygame
pygame.font.init()
screen = pygame.display.set_mode((WIDHT_SERVER_WINDOW, HEIGHT_SERVER_ROOM))
clock = pygame.time.Clock()

#--СОЗДАНИЕ СОКЕТА--
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind((server_ip, 10000))
main_socket.setblocking(False)
main_socket.listen(5)
#--------------------

#--ХРАНЕНИЕ ДАННЫХ--
player_sockets = []
#-------------------

client_connected = False

print('SERVER: STARTED')
running = True
while running:
    clock.tick(FPS)
    screen.fill("black")

    #-----ОБРАБОТЧИК СОБЫТИЙ-----
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            print('SERVER: STOPPED')
    #----------------------------
    #--ПРОВЕРЯЕМ ПОДКЛЮЧЕНИЕ НОВОГО КЛИЕНТА--
    try:
        new_socket, addr = main_socket.accept()
        #new_socket.setblocking(False)
        player_sockets.append(new_socket)
        print('SERVER:', addr, 'connected')
    except:
        pass
    #----------------------------

    #--СЧИТЫВАЕМ КОМАНДЫ КЛИЕНТА--
    try:
        for sock in player_sockets:
            data = sock.recv(1024)
            data = data.decode()
            print('CLIENT:', data, addr)
    except:
        pass
    #----------------------------

    #--ОТПРАВЛЯЕМ СОСТОЯНИЕ ИГРЫ КЛИЕНТУ--
    for sock in player_sockets:
        try:
            message = 'SERVER: НОВОЕ СОСТОЯНИЕ'.encode()
            sock.send(message)
        except:
            print('Error receiving data from client:', addr)
            player_sockets.remove(sock)
            sock.close()
            print('SERVER:', addr, 'disconnected')

    #--ОТПРАВЛЯЕМ СООБЩЕНИЕ КЛИЕНТУ ОБ ПОДКЛЮЧЕНИИ К СЕРВЕРУ--
    for sock in player_sockets:
        if not client_connected:  # если клиент подключился
            sock.send('SERVER: УСПЕШНОЕ ПОДКЛЮЧЕНИЕ'.encode())
            client_connected = True

    pygame.display.update()

# закрываем сервер
pygame.quit()
# закрываем сокеты
main_socket.close()
