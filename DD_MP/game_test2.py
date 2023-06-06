from client_test2 import Network
#import random
#import os
import pygame

pygame.font.init()

W, H = 300, 300


#WIN = pygame.display.set_mode((W,H))

GRID_THEME = (150, 150, 150)

NAME_FONT = pygame.font.SysFont("comicsans", 20)
TIME_FONT = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 26)

pygame.init()

#screen = pygame.display.set_mode((W, H))

def main():
	n_setup = Network()

	# Получение имени пользователя
	while True:
		p_name = input("Please enter your name: ")
		if 0 < len(p_name) < 20:
			break
		else:
			print("Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")
	# Подключение к серверу
	n_setup.n_connect()
	print("Connected to the Server")

	# Основной игровой цикл
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False


		# Отрисовка
		#WIN.fill((255, 255, 255))
		# Здесь можно добавить дополнительные элементы интерфейса и графики
		#pygame.display.update()

	# Отключение от сервера
	n_setup.n_disconnect()
	pygame.quit()
	quit()


# Запуск игры
main()