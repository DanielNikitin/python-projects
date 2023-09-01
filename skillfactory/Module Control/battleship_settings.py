import random

class Config:
    def __init__(self):
        self.SHOW_ENEMY_BOARD = 0  # Отображение игрового поля противника
        self.POS_FREE_MESSAGE = 0  # Отображение Свободного места возле корабля
        self.SUM_ALL_SHIPS = 1  # Отображение Суммы всех кораблей

        self.CHOOSE_ORIENTATION = 1  # Выбор ориентации (нужна для корректной работы user_input)


class BattleshipGame:
    def __init__(self):
        self.LENGTH_OF_SHIPS = [3, 4, 3]  # список кораблей
        self.BOARD_SIZE = 6  # размер игровой доски
        # Словарь, нужен для удобства ввода (так как итерация начинается от 0)
        self.NUMBERS = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5}

        self.PLAYER_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]  # Игровая доска игрока
        self.AI_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]  # ИИ

        self.PLAYER_GUESS_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]  # пустое поле для выстрелов игрока
        self.AI_GUESS_BOARD = [[" "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]  # для ии

        self.config = Config()  # подключаем class Config

    def print_board(self, board):
        # board атрибут делает функцию нейтральной
        # для вызова доски Игрока и ИИ
        # без нее будет возможно привязать только к одной доске
        print("\nДоска Игрока:")
        print("  1 2 3 4 5 6")
        print("-+-+-+-+-+-+-+-")
        row_number = 1  # с какого числа начинаем отсчёт номер столбца
        for row in board:
            print(f"{row_number}|{'|'.join(row)}|")
            # join соединяет элементы списка row и '|'
            row_number += 1
        if self.config.SHOW_ENEMY_BOARD == 1:
            game = BattleshipGame()
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
                    print('Расположите корабль длинной ' + str(ship_length))
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
            # если длинна корабля и коорд столбца больше чем размер доски, то
            if column + ship_length > self.BOARD_SIZE:
                return False  # нельзя
            else:
                return True  # можно
        elif orientation == "V":
            # тоже самое со строчкой (Вертикальная проверка) "V"
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
        orientation = None  # обозначаем сток значение ориентации чтобы не получать ошибку
        if place_ship:
            if self.config.CHOOSE_ORIENTATION == 1:
                #print("PLAYER_INPUT = 1")
                while True:
                    try:
                        orientation = input("Введите ориентацию (H или V): ").upper()  # upper преобразует символы в заглавные
                        if orientation == "H" or orientation == "V":
                            break
                        else:
                            print("Пустой ввод")
                    except TypeError:
                        print('Неверно введена ориентация H или V')

            while True:
                try:
                    row = input("Введите число оси Х от 1 до 6: ")
                    if row in '123456':
                        row = int(row) - 1
                        break
                    else:
                        print("Неверный ввод. Введите целое число для оси Х от 1 до 6.")
                except ValueError:
                    print("Пустой ввод")

            while True:
                try:
                    column = input("Введите число оси Y от 1 до 6: ")
                    if column in '123456':
                        column = self.NUMBERS[column]
                        break
                    elif not column:
                        print("Пустой ввод")
                    else:
                        print("Неверный ввод. Введите целое число для оси Y от 1 до 6.")
                except ValueError:
                    print("Пустой ввод")

            return row, column, orientation  # получаем все данные для ввода строка/столбец/ориентация

    def calculate_total_ship_length(self):  # авто подсчёт кораблей на поле
        return sum(self.LENGTH_OF_SHIPS)  # возврат суммы чисел внутри списка

    def count_hit_ships(self, board):  # подсчёт подбитых кораблей
        count = 0  # изначально 0
        for row in board:
            for column in row:
                if column == "X":  # ищем 'X'
                    count += 1  # если нашел то +1
        return count

    def turn(self, board):
        if board == self.PLAYER_GUESS_BOARD:
            self.config.CHOOSE_ORIENTATION = 0
            #print("PLAYER_INPUT = 0")
            user_input = self.user_input(self.PLAYER_GUESS_BOARD)  # где будем угадывать корабли
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
