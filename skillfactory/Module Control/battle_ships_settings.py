import random
import time

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
        self.ships_count = [Ship("Boost", 3, 3)]#, Ship("Chpoking", 2, 2), Ship("Meow", 1, 1)]  # Имя, размер, жизни

    def input_coordinates(self):
        while True:
            try:
                x = int(input("Введите координату X от 1 до 6: "))
                y = int(input("Введите координату Y от 1 до 6: "))
                r = int(input("Введите положение корабля 1 или 2: "))
                return x, y, r
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числовое значение")

    def input_shoot_coordinates(self):
        while True:
            try:
                x = int(input("Введите координату X от 1 до 6: "))
                y = int(input("Введите координату Y от 1 до 6: "))
                return x, y
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числовое значение")

    def get_ships_count(self):
        return len(self.ships_count)  # len - кол-во элементов в списке


class AIPlayer(Player):
    #  класс AIPlayer является подклассом
    #  (наследует от) класса Player.
    #  Это означает, что AIPlayer получит все свойства и методы,
    #  которые определены в классе Player
    def __init__(self):
        # super вызывает родительский метод init, и передает все атрибуты от родителя
        super().__init__("Компик")  # 'компик' это никнейм атрибута 'p_name' у class Player

    def ai_ship_coordinates(self):
        while True:
            try:
                x = random.randint(1, 6)
                y = random.randint(1, 6)
                r = random.randint(1, 2)
                return x, y, r
            except:
                pass

    def ai_shoot_coordinates(self):
        while True:
            try:
                x = random.randint(1, 6)
                y = random.randint(1, 6)
                return x, y
            except:
                pass


class Board:
    def __init__(self, player):
        # создаем двумерный список, присваемваем функционал для атрибута
        # по принципу действия напоминает генератор (потому что итерируем при вызове)
        # список
        self.game_board = [[" " for _ in range(7)] for _ in range(6)]
        self.player = player
        self.AIPlayer = AIPlayer()

    def print_board(self):
        # наносим горизонтальные ячейки и нумеруем их от 1 до 6
        print("  1 | 2 | 3 | 4 | 5 | 6 | X")
        # 'i+1' для начала отчёта с 1, а не с 0
        for i, current_row in enumerate(self.game_board):
            print(f"{i+1} {current_row[1]} | {current_row[2]} | {current_row[3]}"
                  f" | {current_row[4]} | {current_row[5]} | {current_row[6]} |")
            if i < 6:
                print("-------------------------")

    def place_ship(self, ship, x, y, r):
        try:
            if 1 <= x <= 6 and 1 <= y <= 6 and (r == 1 or r == 2):  # проверяем чтобы ввод был соответсующий для X,Y,R
                if r == 1:  # Если выбрана вертикальная плоскость
                    if ship.length > 0 and y + ship.length - 2 <= 6:
                        for i in range(ship.length):
                            if not self.is_position_free(x, y - 1 + i):
                                print("Нельзя разместить корабль так близко друг к другу 1")
                                return False
                        for i in range(ship.length):
                            if self.game_board[y - 1 + i][x] != ' ':
                                print("Корабль уже находится в этой клетке. Пожалуйста, выберите другие координаты.")
                                return False  # return возвращает на стартовую позицию функции, иначе мы сможем поставить корабль на место, где уже есть корабль
                            self.game_board[y - 1 + i][x] = '■'
                    elif ship.length == 1:
                        self.game_board[y - 1][x] = '■'
                    else:
                        print("Корабль не помещается на доску. Пожалуйста, выберите другие координаты.")
                        return False
                elif r == 2:  # Если выбрана горизонтальная плоскость
                    if ship.length > 0 and x + ship.length - 2 <= 6:
                        for i in range(ship.length):
                            if not self.is_position_free(x + i, y - 1):
                                print("Нельзя разместить корабль так близко друг к другу 2")
                                return False
                        for i in range(ship.length):
                            if self.game_board[y - 1][x + i] != ' ':
                                print("Корабль уже находится в этой клетке. Пожалуйста, выберите другие координаты.")
                                return False  # возвращает на стартовую позицию функции, иначе мы сможем поставить корабль на место, где уже есть корабль
                            self.game_board[y - 1][x + i] = '■'
                    elif ship.length == 1:
                        self.game_board[y - 1][x] = '■'
                    else:
                        print("Корабль не помещается на доску. Пожалуйста, выберите другие координаты.")
                        return False
                return True
            else:
                print("Неверные координаты или ориентация. Пожалуйста, введите числа от 1 до 6 для X и Y, а для R - 1 или 2.")
                return False
        except IndexError:
            print("что-то пошло не так [class Board / def place_ship]")
            return False

    def is_position_free(self, x, y):
        for row in range(max(0, y-1), min(6, y+2)):
            for col in range(max(0, x-1), min(6, x+2)):
                if self.game_board[row][col] in ('■', 'X'):
            #    if self.game_board[row][col] == '■' or self.game_board[row][col] == 'X':  # сначала этот метод использовал, подсказали на счёт 'in'
                    return False
        return True

    def play_game(self):
        # *** Проверка текущего Корабля ***
        current_ships_index = 0  # индекс текущего корабля
        current_ships_count = self.player.get_ships_count()  # текущее кол-во кораблей у player_1
        try:
                for ship in self.player.ships_count:  # итерируем список кораблей у игрока
                    print(f"Осталось расставить кораблей: {current_ships_count - current_ships_index}, текущий {ship.name}")
                    while True:  # Выполняем цикл до тех пор, пока не разместим корабль успешно.
                        # цикл while будет продолжать запрашивать верный ввод координат ля размещения
                        x, y, r = self.player.input_coordinates()  # получаем координаты x,y,r от игрока
                        if self.place_ship(ship, x, y, r):  # проверяем входные данные
                            self.print_board()  # обновляем игровое поле
                            current_ships_index += 1  # добавляем +1 к индексу
                            break  # Выходим из цикла while, так как успешно разместили корабль, и переходим к следующему
        except:
            print("что-то пошло не так [class Board / def play_game]")

    def shoot(self):
        # *** Производим выстрел ***
        start_shooting = True  # показал два варианта исполнения: while true / break, либо кастом переменные
        while start_shooting:
            try:
                x, y = self.player.input_shoot_coordinates()
                if 1 <= x <= 6 and 1 <= y <= 6:  # проверяем предел от 1 до 6
                    # так как счёт начинается с '1', а не с '0', использую формулу [y-1]
                    # 'y-1' это вертикальная координата, 'x' горизонтальная
                    # порядок расстановки y и x, исходя из функционала for в self.game_board
                    # квадратные скобки используются для индексации элементов списков, кортежей и других структур данных, которые итерируются
                    self.game_board[y-1][x] = 'X'
                    print("Выстрел!")
                    time.sleep(0.5)
                    self.print_board()
                    print("Попадание!")
                    start_shooting = False
                else:
                    print("Неверные координаты. Пожалуйста, введите числа от 1 до 6")
            except:
                print("МяВ")

    def ai_shoot(self):
        # *** ИИ производит выстрел ***
        while True:
            try:
                x, y = self.AIPlayer.ai_shoot_coordinates()  # выбираем random значения от 1 до 6
                if self.game_board[y-1][x] == ' ':  # если клетка пустая, то
                    self.game_board[y-1][x] = 'X'
                    print(f"{self.AIPlayer.p_name}: Выстрел!")
                    time.sleep(0.5)
                    self.print_board()
                    break
                else:
                    print(f"{self.AIPlayer.p_name}: Эта клетка уже была выбрана. Повторите выстрел.")
            except ValueError:
                print("МяВ")