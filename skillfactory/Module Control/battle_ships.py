from battle_ships_settings import *


def start_game():
     try:
         # Экземпляр класса Player
         player_1 = Player("Eboisky")
         # Экземпляр класса Board
         game_board = Board(player_1)

         print("Морской Бой Запущен!")

         game_board.player = player_1  # создаем обьект для 'self.player = None'
         game_board.print_board()  #  Рисуем текущее состояние игрового поля
         #print(f"Рядовой {player_1.p_name} расставьте ваши корабли:")
         game_board.play_game()  # Запускаем Игровой прцоесс
         game_board.ai_place_ship()
         #game_board.ai_shoot()
         #game_board.shoot()

     except KeyboardInterrupt:
         print("\nИгра завершена")

#--- Начало игры ---
start_game()