from battle_ships_settings import *


def play_game():
    #class player
    player_1 = Player("Eboisky", 3)
    print("\nВаше имя:", player_1.p_name)

    #class board
    create_board = Board()
    create_board.print_board()

    # Добавляем возможность игроку ставить точку на поле
    while True:
        x, y = player_1.input_coordinates()
        create_board.place_ship(x, y)
        create_board.print_board()


#--- Start Game ---
s = play_game
s()