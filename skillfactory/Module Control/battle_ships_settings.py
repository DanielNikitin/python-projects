#import random
#import time

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass


class Ship:
    def __init__(self, name, length, health):
        self.name = name
        self.length = length
        self.health = health

class Player:
    def __init__(self, p_name):
        self.p_name = p_name
        self.ships_count = [Ship("Boost", 3, 3), Ship("Chpoking", 2, 2), Ship("Meow", 1, 1)]  # Имя, размер, жизни

    def input_coordinates(self):
        while True:
            try:
                x = int(input("Введите координату X от 1 до 6: "))
                y = int(input("Введите координату Y от 1 до 6: "))
                r = int(input("Введите положение корабля 1 или 2: "))
                return x, y, r
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числовое значение")

    def get_ships_count(self):
        return len(self.ships_count)  # len - кол-во элементов в списке


class AIPlayer(Player):
    #  создаем класс AIPlayer, который является подклассом
    #  (наследует от) класса Player.
    #  Это означает, что AIPlayer получит все свойства и методы,
    #  которые определены в классе Player
    def __init__(self):
        # super вызывает родительский метод init, и передает все атрибуты
        super().__init__("Компик")  # 'компик' это никнейм атрибута 'p_name' у class Player


class Board:
    def __init__(self):
        # создаем двумерный список, присваемваем функционал для атрибута
        # по принципу действия напоминает генератор (потому что итерируем при вызове)
        # список
        self.game_board = [[" " for _ in range(7)] for _ in range(6)]
        self.player = None

    def print_board(self):
        # наносим горизонтальные ячейки и нумеруем их от 1 до 6
        print("  1 | 2 | 3 | 4 | 5 | 6 |")
        # 'i+1' для начала отчёта с 1, а не с 0
        for i, current_row in enumerate(self.game_board):
            print(f"{i+1} {current_row[1]} | {current_row[2]} | {current_row[3]}"
                  f" | {current_row[4]} | {current_row[5]} | {current_row[6]} |")
            if i < 6:
                print("-------------------------")

    def shoot(self, x, y):
        try:
            if 1 <= x <= 6 and 1 <= y <= 6:  # проверяем предел от 1 до 6
                # так как счёт начинается с '1', а не с '0', использую формулу [y-1]
                # 'y-1' это вертикальная координата, 'x' горизонтальная
                # порядок расстановки y и x, исходя из функционала for в self.game_board
                # квадратные скобки используются для индексации элементов списков, кортежей и других структур данных, которые итерируются
                self.game_board[y-1][x] = 'X'
                print("Попадание!")
            else:
                print("Неверные координаты. Пожалуйста, введите числа от 1 до 6")
        except:
            pass

    def place_ship(self, ship, x, y, r):
        try:
            if 1 <= x <= 6 and 1 <= y <= 6 and (r == 1 or r == 2):  # проверяем чтобы ввод был соответсующий для X,Y,R
                if r == 1:  # Если выбрана вертикальная ориентация
                    if ship.length > 0 and y + ship.length - 2 <= 6:
                        for i in range(ship.length):
                            if self.game_board[y - 1 + i][x] != ' ':
                                print("Корабль уже находится в этой клетке. Пожалуйста, выберите другие координаты.")
                                return  # без return будет print, но итерация не прекратится, это приведет к установке корабля
                            self.game_board[y - 1 + i][x] = '■'
                    elif ship.length == 1:
                        self.game_board[y - 1][x] = '■'
                    else:
                        print("Корабль не помещается на доску. Пожалуйста, выберите другие координаты.")
                elif r == 2:  # Если выбрана горизонтальная ориентация
                    if ship.length > 0 and x + ship.length - 2 <= 6:
                        for i in range(ship.length):
                            if self.game_board[y - 1][x + i] != ' ':
                                print("Корабль уже находится в этой клетке. Пожалуйста, выберите другие координаты.")
                                return  # без return будет print, но итерация не прекратится, это приведет к установке корабля
                            self.game_board[y - 1][x + i] = '■'
                    elif ship.length == 1:
                        self.game_board[y - 1][x] = '■'
                    else:
                        print("Корабль не помещается на доску. Пожалуйста, выберите другие координаты.")
            else:
                print("Неверные координаты или ориентация. Пожалуйста, введите числа от 1 до 6 для X и Y, а для R - 1 или 2.")
        except IndexError:
            print("Неверные координаты или ориентация. Пожалуйста, введите числа от 1 до 6 для X и Y, а для R - 1 или 2.")

    def play_game(self):
        # *** Блок для проверки текущего Корабля ***
        current_ships_index = 0  # индекс текущего корабля
        current_ships_count = self.player.get_ships_count()  # текущее кол-во кораблей у player_1
        try:
            while current_ships_index < current_ships_count:  # цикл до тех пор, пока ships_index не совпадет с ships_count у player_1
                for ship in self.player.ships_count:  # итерируем список кораблей у игрока
                    print(f"Осталось расставить кораблей: {current_ships_count - current_ships_index}, текущий {ship.name}")
                    x, y, r = self.player.input_coordinates()  # получаем координаты x,y,r от игрока
                    self.place_ship(ship, x, y, r)  # проверяем входные данные
                    self.print_board()  # обновляем игровое поле
                    current_ships_index += 1  # добавляем +1 к индексу
        except:
            print("что-то пошло не так [class Board / def play_game]")