import random

class Config:
    def __init__(self):
        self.SHOW_ENEMY_BOARD = 0  # Отображение игрового поля противника
        self.ai_ship_is_close_message = 1  # Нельзя разместить корабль так близко друг к другу
        self.ai_shoot_coordinate_message = 1   # Координаты стрельбы ИИ
        self.ai_ship_place_coordinate_message = 1  # Координаты расположения корабля
        self.is_position_free_message = 1  # Свободно-ли место для корабля

class BattleshipGame:
    def __init__(self):
        self.LENGTH_OF_SHIPS = [3, 3, 3, 3]
        self.BOARD_SIZE = 6
        self.PLAYER_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.COMPUTER_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.PLAYER_GUESS_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.COMPUTER_GUESS_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.NUMBERS = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5}

    def print_board(self, board):  # board атрибут делает функцию нейтральной
                                   # для вызова доски Игрока и ИИ
        print("\nPlayer Board:")
        print("  1 2 3 4 5 6")
        print("-+-++-+-+-+-+-+")
        row_number = 1
        for row in board:
            print("%d|%s|" % (row_number, "|".join(row)))
            row_number += 1
        game.print_enemy_board()

    def print_enemy_board(self):
        print("\nEnemy Board:")
        print("  1 2 3 4 5 6")
        print("-+-++-+-+-+-+-+")
        row_number = 1
        for row in self.COMPUTER_BOARD:
            print("%d|%s|" % (row_number, "|".join(row)))
            row_number += 1

    def place_ships(self, board):
        for ship_length in self.LENGTH_OF_SHIPS:
            while True:
                if board == self.COMPUTER_BOARD:
                    orientation = random.choice(["H", "V"])
                    row = random.randint(0, self.BOARD_SIZE - 1)
                    column = random.randint(0, self.BOARD_SIZE - 1)
                    if self.check_ship_fit(ship_length, row, column, orientation):
                        if not self.ship_overlaps(board, row, column, orientation, ship_length):
                            if orientation == "H":
                                for i in range(column, column + ship_length):
                                    board[row][i] = "X"
                            else:
                                for i in range(row, row + ship_length):
                                    board[i][column] = "X"
                            break
                else:
                    place_ship = True
                    print('Place the ship with a length of ' + str(ship_length))
                    row, column, orientation = self.user_input(place_ship)
                    if self.check_ship_fit(ship_length, row, column, orientation):
                        if not self.ship_overlaps(board, row, column, orientation, ship_length):
                            if orientation == "H":
                                for i in range(column, column + ship_length):
                                    board[row][i] = "X"
                            else:
                                for i in range(row, row + ship_length):
                                    board[i][column] = "X"
                            self.print_board(self.PLAYER_BOARD)
                            break

    def check_ship_fit(self, ship_length, row, column, orientation):
        if orientation == "H":
            if column + ship_length > self.BOARD_SIZE:
                return False
            else:
                return True
        else:
            if row + ship_length > self.BOARD_SIZE:
                return False
            else:
                return True

    def ship_overlaps(self, board, row, column, orientation, ship_length):
        # Проверяем, есть ли другие корабли рядом с текущим кораблем
        if orientation == "H":
            for i in range(max(0, row - 1), min(self.BOARD_SIZE, row + 2)):
                for j in range(max(0, column - 1), min(self.BOARD_SIZE, column + ship_length + 1)):
                    if board[i][j] == "X":
                        return True
        else:
            for i in range(max(0, row - 1), min(self.BOARD_SIZE, row + ship_length + 1)):
                for j in range(max(0, column - 1), min(self.BOARD_SIZE, column + 2)):
                    if board[i][j] == "X":
                        return True
        return False

    def user_input(self, place_ship):
        if place_ship:
            while True:
                try:
                    orientation = input("Enter orientation (H or V): ").upper()
                    if orientation == "H" or orientation == "V":
                        break
                except TypeError:
                    print('Enter a valid orientation H or V')
            while True:
                try:
                    row = input("Enter the row 1-6 of the ship: ")
                    if row in '123456':
                        row = int(row) - 1
                        break
                except ValueError:
                    print('Enter a valid letter between 1-6')
            while True:
                try:
                    column = input("Enter the column 1-6 of the ship: ").upper()
                    if column in '123456':
                        column = self.NUMBERS[column]
                        break
                except ValueError:
                    print('Enter a valid letter between 1-6')
            return row, column, orientation
        else:
            while True:
                try:
                    row = input("Enter the row 1-6 of the ship: ")
                    if row in '123456':
                        row = int(row) - 1
                        break
                except ValueError:
                    print('Enter a valid letter between 1-6')
            while True:
                try:
                    column = input("Enter the column 1-6 of the ship: ").upper()
                    if column in '123456':
                        column = self.NUMBERS[column]
                        break
                except ValueError:
                    print('Enter a valid letter between 1-6')
            return row, column

    def count_hit_ships(self, board):
        count = 0
        for row in board:
            for column in row:
                if column == "X":
                    count += 1
        return count

    def turn(self, board):
        if board == self.PLAYER_GUESS_BOARD:
            user_input = self.user_input(self.PLAYER_GUESS_BOARD)
            row, column = user_input[0], user_input[1]
            if board[row][column] == "-":
                self.turn(board)
            elif board[row][column] == "X":
                self.turn(board)
            elif self.COMPUTER_BOARD[row][column] == "X":
                board[row][column] = "X"
            else:
                board[row][column] = "-"
        else:
            row, column = random.randint(0, self.BOARD_SIZE - 1), random.randint(0, self.BOARD_SIZE - 1)
            if board[row][column] == "-":
                self.turn(board)
            elif board[row][column] == "X":
                self.turn(board)
            elif self.PLAYER_BOARD[row][column] == "X":
                board[row][column] = "X"
            else:
                board[row][column] = "-"


if __name__ == "__main__":
    print("\n======= Welcome to Battleship =======\n\n")
    game = BattleshipGame()
    game.place_ships(game.COMPUTER_BOARD)
    game.print_board(game.PLAYER_BOARD)
    game.place_ships(game.PLAYER_BOARD)

    while True:
        while True:
            print("\n -- Player Turn --\n")
            print('Guess enemy location\n')
            game.print_board(game.PLAYER_GUESS_BOARD)
            game.turn(game.PLAYER_GUESS_BOARD)
            break
        if game.count_hit_ships(game.PLAYER_GUESS_BOARD) == 17:
            print("You win!")
            break

        while True:
            print("\n-- Computer Turn --\n")
            game.turn(game.COMPUTER_GUESS_BOARD)
            break
        game.print_board(game.COMPUTER_GUESS_BOARD)
        if game.count_hit_ships(game.COMPUTER_GUESS_BOARD) == 17:
            print("Sorry, the computer won.")
            break
