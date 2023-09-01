import random

class Config:
    def __init__(self):
        self.SHOW_ENEMY_BOARD = 0  # Отображение игрового поля противника
        self.POS_FREE_MESSAGE = 0  # Свободно-ли место возле корабля
        self.CHOOSE_ORIENTATION = 1  # Выбор ориентации


class BattleshipGame:
    def __init__(self):
        self.LENGTH_OF_SHIPS = [3]
        self.BOARD_SIZE = 6
        self.PLAYER_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.AI_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.PLAYER_GUESS_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.AI_GUESS_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        # Словарь, нужен для удобства ввода (так как итерация начинается от 0)
        self.NUMBERS = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5}

        self.config = Config()

    def print_board(self, board):  # board атрибут делает функцию нейтральной
                                   # для вызова доски Игрока и ИИ
        print("\nPlayer Board:")
        print("  1 2 3 4 5 6")
        print("-+-++-+-+-+-+-+")
        row_number = 1
        for row in board:
            print(f"{row_number}|{'|'.join(row)}|")
            row_number += 1
        if self.config.SHOW_ENEMY_BOARD == 1:
            game.print_enemy_board()

    def print_enemy_board(self):
        print("\nEnemy Board:")
        print("  1 2 3 4 5 6")
        print("-+-++-+-+-+-+-+")
        row_number = 1  # число для начала итерации строки
        for row in self.AI_BOARD:
            print(f"{row_number}|{'|'.join(row)}|")
            row_number += 1

    def place_ships(self, board):
        for ship_length in self.LENGTH_OF_SHIPS:
            while True:
                if board == self.AI_BOARD:
                    orientation = random.choice(["H", "V"])
                    row = random.randint(0, self.BOARD_SIZE - 1)
                    column = random.randint(0, self.BOARD_SIZE - 1)
                    if self.check_ship_fit(ship_length, row, column, orientation):
                        if not self.ship_is_near(board, row, column, orientation, ship_length):
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
                    print('------------------')
                    row, column, orientation = self.user_input(place_ship)
                    if self.check_ship_fit(ship_length, row, column, orientation):
                        if not self.ship_is_near(board, row, column, orientation, ship_length):
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

    def ship_is_near(self, board, row, column, orientation, ship_length):
        # Проверяем, есть ли другие корабли рядом с текущим кораблем
        # board - где проверяем, row/column - координаты корабля, orientation и ship_length - ориентация и длинна корабля
        if orientation == "H":
            for i in range(max(0, row - 1), min(self.BOARD_SIZE, row + 2)):
        # цикл для того, чтобы проверить три строки:
        # одну выше текущей строки, текущую строку и одну ниже текущей строки.
                for j in range(max(0, column - 1), min(self.BOARD_SIZE, column + ship_length + 1)):
                    if board[i][j] == "X":
                        if self.config.POS_FREE_MESSAGE == 1:
                            print("Нельзя разместить корабль так близко друг к другу (H)")
                        # проверка на 'X' в ячейке
                        return True  # если есть, то True
        else:  # для вертикали
            for i in range(max(0, row - 1), min(self.BOARD_SIZE, row + ship_length + 1)):
                for j in range(max(0, column - 1), min(self.BOARD_SIZE, column + 2)):
                    if board[i][j] == "X":
                        if self.config.POS_FREE_MESSAGE == 1:
                            print("Нельзя разместить корабль так близко друг к другу (V)")
                        return True
        return False  # если пусто, False

    def user_input(self, place_ship):
        orientation = None
        if place_ship:
            if self.config.CHOOSE_ORIENTATION == 1:
                print("PLAYER_INPUT = 1")
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
            self.config.CHOOSE_ORIENTATION = 0
            print("PLAYER_INPUT = 0")
            user_input = self.user_input(self.PLAYER_GUESS_BOARD)
            row, column = user_input[0], user_input[1]  # [0] это строка [1] столбец
            if board[row][column] == "-":
                self.turn(board)
            elif board[row][column] == "X":
                self.turn(board)
            elif self.AI_BOARD[row][column] == "X":
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
    game.place_ships(game.AI_BOARD)
    game.print_board(game.PLAYER_BOARD)
    game.place_ships(game.PLAYER_BOARD)

    while True:
        while True:
            print("\n -- Player Turn --")
            print('Guess enemy location\n')
            game.print_board(game.PLAYER_GUESS_BOARD)
            game.turn(game.PLAYER_GUESS_BOARD)
            break
        if game.count_hit_ships(game.PLAYER_GUESS_BOARD) == 17:
            print("You win!")
            break

        while True:
            print("\n-- Computer Turn --\n")
            game.turn(game.AI_GUESS_BOARD)
            break
        game.print_board(game.AI_GUESS_BOARD)
        if game.count_hit_ships(game.AI_GUESS_BOARD) == 17:
            print("Sorry, the computer won.")
            break
