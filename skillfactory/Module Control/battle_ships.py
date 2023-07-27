from battle_ships_settings import *


def play_game():
     try:
         player_1 = Player("Eboisky")
         print("\nВаше имя:", player_1.p_name)

         game_board = Board()  # Запускаем Игровой Интерфейс
         game_board.player = player_1  # создаем обьект для 'self.player = None'

         game_board.print_board()  #  Рисуем текущее состояние игрового поля
         print(f"Рядовой {player_1.p_name} расставьте ваши корабли:")
         game_board.play_game()  # Запускаем Игровой прцоесс

     except KeyboardInterrupt:
         print("\nИгра завершена")

#--- Начало игры ---
play_game()

# while True:
# Производим выстрел
#     x, y = player_1.input_coordinates()
#     create_board.shoot(x, y)
#     create_board.print_board()