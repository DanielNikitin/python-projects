import time

def print_board(game_board):
    print("  0   1   2 ")
    for i, current_row in enumerate(game_board):
        print(f"{i} {current_row[0]} | {current_row[1]} | {current_row[2]}")
        if i < 2:
            print("  ---------")

def check_winner(game_board, player):
    for i in range(3):
        if all([game_board[i][j] == player for j in range(3)]):  # Проверка по горизонтали
            return True
        if all([game_board[j][i] == player for j in range(3)]):  # Проверка по вертикали
            return True
    if all([game_board[i][i] == player for i in range(3)]):  # Проверка по диагонали (слева направо)
        return True
    if all([game_board[i][2 - i] == player for i in range(3)]):  # Проверка по диагонали (справа налево)
        return True
    return False

def is_board_full(game_board):
    for row in game_board:
        for cell in row:
            if cell == " ":
                return False
    return True

def restart_game():
    print("Игра будет перезапущена через:")
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)
    print("REPLAY!")
    time.sleep(1)
    play_game()

def play_game():
    game_board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "Y"]
    current_player = 0

    while True:
        print_board(game_board)
        player = players[current_player]
        while True:
            row = int(input(f"Игрок {player}, введите номер строки (0, 1, 2): "))  # строка
            col = int(input(f"Игрок {player}, введите номер столбца (0, 1, 2): ")) # столб
            if 0 <= row < 3 and 0 <= col < 3:
                if game_board[row][col] == " ":
                    break
                else:
                    print("Эта клетка уже занята. Попробуйте снова.")
            else:
                print("Неверные координаты. Попробуйте снова.")

        game_board[row][col] = player
        # указываем на игровом поле ячейку с игроком, который сделал ход

        if check_winner(game_board, player):
            print_board(game_board)
            print(f"Игрок {player} победил!")
            time.sleep(1)
            restart_game()
        elif is_board_full(game_board):
            print_board(game_board)
            print("Ничья!")
            time.sleep(1)
            restart_game()
        else:
            current_player = 1 - current_player

if __name__ == "__main__":
    play_game()