#import random
#import time

class Board:
    def __init__(self):
        # создаем ячейки
        self.game_board = [[" " for _ in range(7)] for _ in range(6)]

    def print_board(self):
        # наносим ячейки и нумеруем их от 1 до 6
        print("  1 | 2 | 3 | 4 | 5 | 6 |")
        for i, current_row in enumerate(self.game_board):
            print(f"{i+1} {current_row[1]} | {current_row[2]} | {current_row[3]}"
                  f" | {current_row[4]} | {current_row[5]} | {current_row[6]} |")
            if i < 6:
                print("-------------------------")

    def place_ship(self, x, y):
        if 1 <= x <= 6 and 1 <= y <= 6:
            self.game_board[y - 1][x] = 'X'
        else:
            print("Неверные координаты. Пожалуйста, введите числа от 1 до 6")


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass


class Player:
    def __init__(self, p_name, ships_count):
        self.p_name = p_name
        self.ships_count = ships_count

    def input_coordinates(self):
        while True:
            try:
                x = int(input("Введите координату X (от 1 до 6): "))
                y = int(input("Введите координату Y (от 1 до 6): "))
                return x, y
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числовое значение")


class Ship:
    def __init__(self, length, health):
        self.length = length
        self.health = health


