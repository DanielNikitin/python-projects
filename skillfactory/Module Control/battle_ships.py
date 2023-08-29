from battle_ships_settings import *


def start_game():
     try:
         # Экземпляр класса Player
         player_1 = Player("Eboisky")
         # Экземпляр класса Board
         game_board = Board(player_1)

         print("Морской Бой Запущен!")

         game_board.player = player_1  # создаем обьект для 'self.player = None'
         game_board.print_board()  # Передаем поля игрока и ИИ
         #print(f"Рядовой {player_1.p_name} расставьте ваши корабли:")
         game_board.switch_current_board()
         game_board.ai_place_ship()
         #game_board.get_current_board()
         #game_board.get_current_board()
         #game_board.player_place_ship()
         #while True:
         #game_board.player_place_ship()
         #game_board.ai_shoot()
         #game_board.ai_shoot()
         #game_board.shoot()

     except KeyboardInterrupt:
         print("\nQuit")

#--- Начало игры ---
start_game()