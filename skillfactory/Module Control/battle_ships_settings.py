import random
import time

class Config:
    def __init__(self):
        self.ai_ship_place_message = 0  # 1/0 - Булевая для print("Нельзя разместить корабль так близко друг к другу"


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
                            # Имя, размер, жизни
        self.ships_count = [Ship("Boost", 3, 3),
                            Ship("Chpoking", 2, 2), Ship("Fire", 2, 2),
                            Ship("Meow", 1, 1), Ship("Кусь", 1, 1), Ship("Чики-бони", 1, 1), Ship("Boomer", 1, 1)]

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
    def __init__(self, board_instance):
        # super вызывает родительский метод init, и передает все атрибуты от родителя
        super().__init__("Компик")  # 'компик' это никнейм атрибута 'p_name' у class Player
        self.board_instance = board_instance  # соединяемся с классом Board

    def ai_ship_coordinates(self, ship):
        while True:
            try:
                valid_coordinates = []

                for x in range(1, 7):
                    for y in range(1, 7):
                        for r in range(1, 3):
                            if self.ai_is_valid_placement(x, y, r, ship):
                                valid_coordinates.append((x, y, r))
                if valid_coordinates:
                    return random.choice(valid_coordinates)
            except Exception as e:
                print(f"Ошибка: {e} ")

    def ai_is_valid_placement(self, x, y, r, ship):
        if r == 1:  # вертикальная ориентация
            if y + ship.length - 1 <= 6:
                for row in range(y, y + ship.length):
                    if not self.ai_is_position_free(x, row, ship.length, r):
                        return False
            else:
                return False
        elif r == 2:  # горизонтальная ориентация
            if x + ship.length - 1 <= 6:
                for col in range(x, x + ship.length):
                    if not self.ai_is_position_free(col, y, ship.length, r):
                        return False
            else:
                return False
        return True

    def ai_shoot_coordinates(self):
        while True:
            try:
                x = random.randint(1, 6)
                y = random.randint(1, 6)
                return x, y
            except:
                pass

    def ai_is_position_free(self, x, y, ship_length, r):
        # Используем self.board_instance.game_board вместо self.game_board
        if r == 1:
            for row in range(max(0, y - 1), min(6, y + ship_length)):
                if self.board_instance.ai_board[row][x] in ('■', 'X'):
                    return False
        elif r == 2:
            for col in range(max(0, x - 1), min(6, x + ship_length)):
                if self.board_instance.ai_board[y - 1][col] in ('■', 'X'):
                    return False
        return True


class Board:
    def __init__(self, player):
        # создаем двумерный список, присваемваем функционал для атрибута
        # по принципу действия напоминает генератор (потому что итерируем при вызове)
        # список
        self.player_board = [[" " for _ in range(7)] for _ in range(6)]
        self.ai_board = [[" " for _ in range(7)] for _ in range(6)]
        self.player = player
        self.aiplayer = AIPlayer(self) # Создание экземпляра класса AIPlayer
        self.config = Config()  # Создание экземпляра класса Config
        self.current_board = self.ai_board if self.aiplayer != self.player else self.player_board

    def print_board(self):
        print("           [Поле Игрока]        :             [Поле ИИ]")
        print("    1 | 2 | 3 | 4 | 5 | 6 | X   |      1 | 2 | 3 | 4 | 5 | 6 | X")
        for i in range(6):
            player_row = f"{i + 1} "
            ai_row = f"{i + 1} "
            for j in range(6):
                player_row += f"| {self.player_board[i][j+1]} "
                ai_row += f"| {self.ai_board[i][j]} "
            player_row += "|"
            ai_row += "|"
            print(player_row.ljust(30), " | ", ai_row.ljust(30))  # ljust выраввнивание по левому краю
            if i != 5:
                print("-------------------------     |    -------------------------")
        print("Y                                  Y")

    def place_ship(self, ship, x, y, r):
        try:
            for i in range(ship.length):
                print(f"Попытка {i + 1}: Размещение корабля '{ship.name}' в ({x}, {y - 1 + i})")
            if 1 <= x <= 6 and 1 <= y <= 6 and (r == 1 or r == 2):  # проверяем чтобы ввод был соответсующий для X,Y,R
                if r == 1:  # Если выбрана вертикальная плоскость
                    if ship.length > 0 and y + ship.length - 2 <= 6:
                        for i in range(ship.length):
                            if not self.is_position_free(x, y - 1 + i):
                                if self.config.ai_ship_place_message == 1:
                                    print("Нельзя разместить корабль так близко друг к другу (верт)")  # вертикаль
                                return False
                        for i in range(ship.length):
                            if self.current_board[y - 1 + i][x] != ' ':
                                print("Корабль уже находится в этой клетке. Пожалуйста, выберите другие координаты.")
                                return False  # return возвращает на стартовую позицию функции, иначе мы сможем поставить корабль на место, где уже есть корабль
                            self.current_board[y - 1 + i][x] = '■'
                    elif ship.length == 1:
                        self.current_board[y - 1][x] = '■'
                    else:
                        print("Корабль не помещается на доску. Пожалуйста, выберите другие координаты.")
                        return False
                elif r == 2:  # Если выбрана горизонтальная плоскость
                    if ship.length > 0 and x + ship.length - 2 <= 6:
                        for i in range(ship.length):
                            if not self.is_position_free(x + i, y - 1):
                                if self.config.ai_ship_place_message == 1:
                                    print("Нельзя разместить корабль так близко друг к другу (гор)")  # горизонт
                                return False
                        for i in range(ship.length):
                            if self.current_board[y - 1][x + i] != ' ':
                                print("Корабль уже находится в этой клетке. Пожалуйста, выберите другие координаты.")
                                return False  # возвращает на стартовую позицию функции, иначе мы сможем поставить корабль на место, где уже есть корабль
                            self.current_board[y - 1][x + i] = '■'
                    elif ship.length == 1:
                        self.current_board[y - 1][x] = '■'
                    else:
                        print("Корабль не помещается на доску. Пожалуйста, выберите другие координаты.")
                        return False
                return True
            else:
                print("Неверные координаты или ориентация. Пожалуйста, введите числа от 1 до 6 для X и Y, а для R - 1 или 2.")
                return False
        except Exception as e:
            print(f"Ошибка: {e}")
            return False

    def is_position_free(self, x, y):  # проверка на свободную ячейку по указанным координатам
        for col in range(max(0, x-1), min(6, x+2)):  # перебор по горизонтали (х)
            for row in range(max(0, y - 1), min(6, y + 2)):  # перебор по вертикали (y)
                if self.player_board[row][col] in ('■', 'X'):  # если в ячейке есть что-то, то return False, и проверяем заново
            #    if self.game_board[row][col] == '■' or self.game_board[row][col] == 'X':  # сначала этот метод использовал
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
        except Exception as e:
            print(f"Ошибка: {e}")

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
                    self.player_board[y-1][x] = 'X'
                    print("Выстрел!")
                    time.sleep(0.5)
                    self.print_board()
                    print("Попадание!")
                    start_shooting = False
                else:
                    print("Неверные координаты. Пожалуйста, введите числа от 1 до 6")
            except Exception as e:
                print(f"Ошибка: {e}")

    def ai_shoot(self):
        # *** ИИ производит выстрел ***
        # первым написал эту функцию, она более простая для написания и построения логики
        while True:
            try:
                x, y = self.aiplayer.ai_shoot_coordinates()  # выбираем random значения от 1 до 6
                if self.player_board[y-1][x] == ' ':  # если клетка пустая, то
                    self.player_board[y-1][x] = 'X'
                    print(f"{self.aiplayer.p_name}: Выстрел!")
                    time.sleep(0.5)
                    self.print_board()
                    break
                else:
                    print(f"{self.aiplayer.p_name}: Эта клетка уже была выбрана. Повторите выстрел.")
            except Exception as e:
                print(f"Ошибка: {e}")

    def ai_place_ship(self):
        # *** ИИ расставляет корабли ***
        try:
            for ship in self.aiplayer.ships_count:
                while True:
                    time.sleep(0)
                    #print(f"{self.AIPlayer.p_name}: Расставляю Корабли")
                    x, y, r = self.aiplayer.ai_ship_coordinates(ship)
                    if self.place_ship(ship, x, y, r):
                        break
            self.print_board()
        except Exception as e:
            print(f"Ошибка: {e}")
