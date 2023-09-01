from battleship_settings import *


def start_game():
     try:
         if __name__ == "__main__":
             print("\n======= BattleShip Game V1 =======\n")
             game = BattleshipGame()
             game.place_ships(game.AI_BOARD)
             game.print_board(game.PLAYER_BOARD)
             game.place_ships(game.PLAYER_BOARD)

             while True:
                 while True:
                     print("\n -- Ход Игрока --")
                     print('')
                     game.print_board(game.PLAYER_GUESS_BOARD)
                     game.turn(game.PLAYER_GUESS_BOARD)
                     break
                 if game.count_hit_ships(game.PLAYER_GUESS_BOARD) == game.calculate_total_ship_length():
                     print("Вы выйграли!")
                     break

                 while True:
                     print("\n-- Ход ИИ --")
                     game.turn(game.AI_GUESS_BOARD)
                     break
                 game.print_board(game.AI_GUESS_BOARD)
                 if game.count_hit_ships(game.AI_GUESS_BOARD) == game.calculate_total_ship_length():
                     print("ИИ Выйграл!")
                     break

     except KeyboardInterrupt:
         print("\nQuit")

#--- Начало игры ---
start_game()